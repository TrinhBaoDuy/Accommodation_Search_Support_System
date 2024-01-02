from threading import activeCount

from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from ASSSs import serializers, paginators
from ASSSs.models import House, Image, Post, Discount, PostingPrice, User, Follow, Booking, Role, Comment
from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from twilio.rest import Client
import random
import datetime
# Create your views here.


class HouseViewSet(viewsets.ViewSet):
    queryset = House.objects.filter(active=True).all()
    serializer_class = serializers.HouseSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new house",
        request_body=serializers.HouseSerializer,
        responses={
            201: serializers.HouseSerializer(),
            400: "Bad request"
        }
    )
    @action(methods=['post'], url_name='create-house', detail=False)
    def create_house(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method='get',
        operation_description="Get a list of houses",
        manual_parameters=[
            openapi.Parameter(
                name="address",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="address",
                required=False,
            ),
        ],
        responses={
            200: serializers.HouseSerializer(many=True),
            400: "Bad request"
        }
    )
    @action(methods=['get'], detail=False)
    def get_queryset(self, request):
        queryset = self.queryset

        address = request.query_params.get("address")
        if address:
            queryset = queryset.filter(address__icontains=address)

        acreage = request.query_params.get("acreage")
        if acreage:
            queryset = queryset.filter(acreage__icontains=acreage)

        return Response(serializers.HouseSerializer(queryset, many=True).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='images')
    def images(self, request, pk):
        house = self.queryset.filter(id=pk).first()
        if not house:
            return Response(status=status.HTTP_404_NOT_FOUND)
        images = house.image_set.all()
        return Response(serializers.ImageSerializerShow(images, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ViewSet):
    queryset = Image.objects.filter(active=True).all()
    serializer_class = serializers.ImageSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    @swagger_auto_schema(
        operation_description="Push Images House",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Enter the image",
                required=True,
            ),
            openapi.Parameter(
                name="house",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="house_id",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['post'], url_name='push-images-for-house', detail=False)
    def push_images_for_house(self, request):
        user = request.user
        new_image = request.FILES.get('image')
        house_id = request.data.get('house')

        if not new_image:
            return Response("Image is required.", status=status.HTTP_400_BAD_REQUEST)

        try:
            house = House.objects.get(id=house_id, active=True)
        except House.DoesNotExist:
            return Response("House does not exist.", status=status.HTTP_400_BAD_REQUEST)

        # self.serializer_class().push_images_for_house(house_id, new_image)
        serializer = serializers.ImageSerializer(data={
            'imageURL': new_image,
            'house': house_id
        })

        if serializer.is_valid():
            serializer.save()
            return Response("Images for house created successfully.", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializers.ImageSerializer().data, status=status.HTTP_200_OK)

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("houseID")
        if q:
            queries = queries.filter(house__id=q)

        return queries


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        serializer = serializers.PostSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='list-post-not-accepted', detail=False)
    def list_post_not_accepted(self, request):
        queryset = self.queryset.filter(status=0).all()
        serializer = serializers.PostSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='list-post-accepted', detail=False)
    def list_post_accepted(self, request):
        queryset = self.queryset.filter(status=1).filter(postingdate__lte=datetime.datetime.now(), expirationdate__gte=datetime.datetime.now()).order_by('-postingdate').all()
        serializer = serializers.PostSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Accept Post",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Post Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['patch'], detail=False, url_path='accept-post')
    def accept_post(self, request):
        pk = request.data.get('pk')

        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        if post.status != 0:
            return Response("This post has been published.", status=status.HTTP_400_BAD_REQUEST)

        self.serializer_class().accept_post(post)
        post.refresh_from_db()

        return Response("Accept this post successfully", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Not Accept Post",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Post Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['patch'], detail=False, url_path='not-accept-post')
    def not_accept_post(self, request):
        pk = request.data.get('pk')

        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        if post.status == 0:
            return Response("This post has been not accepted.", status=status.HTTP_400_BAD_REQUEST)

        self.serializer_class().unaccept_post(post)
        post.refresh_from_db()

        return Response("Not Accept this post successfully", status=status.HTTP_200_OK)

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("address")
        if q:
            queries = queries.filter(house__address__icontains=q)
        return queries

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=serializers.PostSerializer,
        responses={
            201: openapi.Response(
                description="Post created successfully",
                schema=serializers.PostSerializer
            ),
            400: openapi.Response(
                description="Bad request"
            )
        }
    )
    @action(methods=['post'], url_name='create-post', detail=False)
    def create_post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete Post",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Post Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['post'], url_path='delete-post', detail=False)
    def delete_post(self, request):
        pk = request.data.get('pk')

        try:
            post = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        if post.status != 1:
            return Response("Your post is awaiting confirmation. Please delete after the article has been posted", status=status.HTTP_404_NOT_FOUND)

        post.delete()

        return Response("Delete post successfully.", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='comments')
    def comment(self, request, pk):
        post = self.queryset.filter(id=pk).first()
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = post.comment_set.all()
        return Response(serializers.CommentSerializerShow(comments, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet):
    queryset = Comment.objects.filter(active=True).all()
    serializer_class = serializers.CommentSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    @swagger_auto_schema(
        operation_description="Create a new Comment",
        request_body=serializers.CommentSerializer,
        responses={
            201: openapi.Response(
                description="Comment created successfully",
                schema=serializers.CommentSerializer
            ),
            400: openapi.Response(
                description="Bad request"
            )
        }
    )
    @action(methods=['post'], url_name='create-comment', detail=False)
    def create_comment(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete Comment",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Comment Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['post'], url_path='delete-comment', detail=False)
    def delete_comment(self, request):
        pk = request.data.get('pk')

        try:
            comment = self.queryset.get(id=pk)
        except Comment.DoesNotExist:
            return Response("This Comment does not exist.", status=status.HTTP_404_NOT_FOUND)

        if comment.active == 0:
            return Response("The comment has been deleted", status=status.HTTP_404_NOT_FOUND)

        comment.delete()

        return Response("Delete comment successfully.", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Change value Comment",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="Comment Id",
                required=True,
            ),
            openapi.Parameter(
                name="value",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Comment value",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['patch'], url_path='change-value-comment', detail=False)
    def change_value_comment(self, request):
        pk = request.data.get('pk')
        value = request.data.get('value')

        try:
            comment = self.queryset.get(id=pk)
        except Comment.DoesNotExist:
            return Response("This comment does not exist.", status=status.HTTP_404_NOT_FOUND)

        if comment.active == 0:
            return Response("The comment has been deleted", status=status.HTTP_404_NOT_FOUND)

        self.serializer_class().change_value_comment(comment, value)
        comment.refresh_from_db()

        return Response("Change value comment successfully.", status=status.HTTP_200_OK)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None


class PostingPriceViewSet(viewsets.ModelViewSet):
    queryset = PostingPrice.objects.all()
    serializer_class = serializers.PostingPriceSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    def get_permissions(self):
        if self.action.__eq__('current_user') or self.action.__eq__('reset_password'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @swagger_auto_schema(
        operation_description="Create a new user",
        request_body=serializers.UserSerializer,
        responses={
            201: openapi.Response(
                description="User created successfully",
                schema=serializers.UserSerializer
            ),
            400: openapi.Response(
                description="Bad request"
            )
        }
    )
    @action(methods=['post'], url_name='create-user', detail=False)
    def create_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Retrieve a user by ID",
        responses={
            200: openapi.Response(
                description="User retrieved successfully",
                schema=serializers.UserSerializer
            ),
            404: openapi.Response(
                description="User not found"
            )
        }
    )
    @action(methods=['get'], url_name='get-user', detail=True)
    def get_user_by_id(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get the current user",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            )
        ],
        responses={
            200: openapi.Response(
                description="SMS sent with password reset instructions",
            ),
            400: openapi.Response(
                description="User with this phone number does not exist",
            ),
        }
    )
    @action(methods=['get'], url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializers.UserSerializer(request.user).data)

    @swagger_auto_schema(
        operation_description="Reset password",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=True,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="old_password",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Old password",
                required=True
            ),
            openapi.Parameter(
                name="new_password",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="New password",
                required=True
            ),
            openapi.Parameter(
                name="new_password_again",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Re-enter new password",
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Password updated successfully"
            ),
            400: openapi.Response(
                description="Invalid old password"
            )
        }
    )
    @action(methods=['patch'], url_path='reset-password', detail=False)
    def reset_password(self, request):
        user = request.user

        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        new_password_again = request.data.get('new_password_again')

        if not user.check_password(old_password):
            return Response("Invalid old password", status=status.HTTP_400_BAD_REQUEST)

        if not new_password.__eq__(new_password_again):
            return Response("The new password patterns do not match", status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response("Password updated successfully", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Send OTP Forgot password",
        manual_parameters=[
            openapi.Parameter(
                name="phone_number",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="phone_number",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="SMS sent with password reset instructions",
            ),
            400: openapi.Response(
                description="User with this phone number does not exist",
            ),
        }
    )
    @action(methods=['post'], url_path='send-OTP-forgot-password', detail=False)
    def forgot_password(self, request):
        phone_number = request.data.get('phone_number')
        Country_Code='+84'
        try:
            user = User.objects.get(phonenumber=phone_number)
        except User.DoesNotExist:
            return Response("User with this phone number does not exist.", status=status.HTTP_400_BAD_REQUEST)

        digits = "0123456789"
        otp = ""
        for i in range(6):
            otp += random.choice(digits)

        # Gửi tin nhắn SMS chứa hướng dẫn đặt lại mật khẩu
        account_sid = 'AC1c77c96392cffe33999c3ca1b6635e7d'
        auth_token = '474fe6134a659fef4dadf1fed37425c7'
        from_number = '+17247172226'

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=f"Please use the following OTP for verification: {otp}. This OTP will expire in 60 seconds. Please do not share this OTP with anyone. Thank you.",
            from_=from_number,
            to=Country_Code+phone_number
        )

        # Lưu OTP và số điện thoại vào session
        request.session['phone_number'] = phone_number
        request.session['otp'] = otp
        request.session['otp_timestamp'] = datetime.datetime.now()
        request.session.modified = True

        # Chuyển hướng đến endpoint reset-password với OTP và số điện thoại
        return HttpResponseRedirect('/check-OTP-change-forgot-password')

    @swagger_auto_schema(
        operation_description="Check OTP And Change password",
        manual_parameters=[
            openapi.Parameter(
                name="otp_check",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Enter the OTP just notified in SMS",
                required=True,
            ),
            openapi.Parameter(
                name="new_password",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Enter the new password",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="SMS sent with password reset instructions",
            ),
            400: openapi.Response(
                description="User with this phone number does not exist",
            ),
        }
    )
    @action(methods=['post'], url_path='check-OTP-change-forgot-password', detail=False)
    def check_OTP_change_forgot_password(self, request):
        phone_number = request.session.get('phone_number')
        otp = request.session.get('otp')
        otp_check = request.data.get('otp_check')
        new_password = request.data.get('new_password')
        timestamp = request.session.get('otp_timestamp')

        if not phone_number or not otp:
            return Response("OTP expired or invalid.", status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phonenumber=phone_number)
        except User.DoesNotExist:
            return Response("User with this phone number does not exist.", status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra tính hợp lệ của OTP
        if not otp == otp_check:
            return Response("Invalid OTP.", status=status.HTTP_400_BAD_REQUEST)

        # Kiểm tra hiệu lực của OTP
        current_time = datetime.datetime.now()
        time_diff = current_time - timestamp
        if time_diff.seconds > 60:  # Kiểm tra nếu đã qua hơn 1 phút
            return Response("OTP expired.", status=status.HTTP_400_BAD_REQUEST)

        # Đặt lại mật khẩu của người dùng
        user.set_password(new_password)
        user.save()

        # Xóa OTP và số điện thoại khỏi session
        del request.session['phone_number']
        del request.session['otp']
        request.session.modified = True

        return Response("Password reset successful.", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update Avatar",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="avatar",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                description="Enter the new avatar",
                required=True,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=serializers.UserSerializer
            )
        }
    )
    @permission_classes([IsAuthenticated])
    @action(methods=['patch'], url_path='update-avatar', detail=False)
    def update_avatar(self, request):
        user = request.user
        new_avatar = request.FILES.get('avatar')
        if not new_avatar:
            return Response("Avatar is required.", status=status.HTTP_400_BAD_REQUEST)

        self.serializer_class().update_avatar(user, new_avatar)
        user.refresh_from_db()

        return Response(serializers.UserSerializer(user).data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get the current user",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            )
        ],
        responses={
            200: openapi.Response(
                description="Succes",
            ),
            400: openapi.Response(
                description="User does not exist",
            ),
        }
    )
    @action(methods=['get'], detail=False, url_path='myposts')
    def myposts(self, request):
        user = self.queryset.filter(id=request.user.id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        posts = user.post_set.all()
        return Response(serializers.PostSerializerShow(posts, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


    @action(methods=['get'], detail=True, url_path='posts')
    def posts(self, request, pk):
        user = self.queryset.filter(id=pk).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        posts = user.post_set.all()
        return Response(serializers.PostSerializerShow(posts, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ViewSet):
    queryset = Follow.objects.filter(active=True).all()
    serializer_class = serializers.FollowSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    @swagger_auto_schema(
        operation_description="Get Followers By Current User",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=serializers.FollowSerializer
            )
        }
    )
    @action(methods=['get'], detail=False, url_path='followers-by-current-user')
    def followers_by_current_user(self, request):
        current_user = request.user
        try:
            followers = self.queryset.filter(followeduser=current_user)
            serializer = serializers.FollowSerializerShow(followers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response("User has no followers", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get Followeduser By Current User",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=False,
                default="Bearer your_token_here"
            )
        ],
        responses={
            200: openapi.Response(
                description="Successful operation",
                schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['get'], detail=False, url_path='followeduser-by-current-user')
    def followeduser_by_current_user(self, request):
        current_user = request.user
        try:
            followeduser = self.queryset.filter(follower=current_user)
            serializer = serializers.FollowSerializerShow(followeduser, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response("User has no followeduser", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new Follow",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=True,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="followed_user",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="ID User",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="Follow created"
            ),
            400: openapi.Response(
                description="Follow fall"
            )
        }
    )
    @action(methods=['post'], url_path='create-or-update-follow', detail=False)
    def create_or_update_follow(self, request):
        current_user = request.user
        followed_user_id = request.data.get('followed_user')

        try:
            followed_user = User.objects.get(id=followed_user_id)
        except followed_user.DoesNotExist:
            return Response("The followed user does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if current_user.following.filter(followeduser=followed_user, active=True).exists():
            return Response("You have already followed this user.", status=status.HTTP_400_BAD_REQUEST)

        existing_follow = current_user.following.filter(followeduser=followed_user).first()
        if existing_follow:
            if existing_follow.active:
                return Response("You have already followed this user.", status=status.HTTP_400_BAD_REQUEST)
            else:
                existing_follow.active = True
                existing_follow.save()
                return Response("Follow updated successfully at "+str(datetime.date.today().strftime('%d/%m/%Y')), status=status.HTTP_200_OK)

        if current_user.__eq__(followed_user):
            return Response("You cannot follow yourself.", status=status.HTTP_400_BAD_REQUEST)

        if current_user.__eq__(followed_user):
            return Response("You cannot follow yourself.", status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.FollowSerializer(data={
            'follower': current_user.id,
            'followeduser': followed_user_id
        })

        if serializer.is_valid():
            serializer.save()
            return Response("Follow created successfully.", status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="UnFollow",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=True,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="followed_user",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="ID User",
                required=True
            ),
        ],
        responses={
            200: openapi.Response(
                description="UnFollow successfully"
            ),
            400: openapi.Response(
                description="UnFollow fall"
            )
        }
    )
    @action(methods=['post'], url_path='un-follow', detail=False)
    def un_follow(self, request):
        current_user = request.user
        followed_user_id = request.data.get('followed_user')

        try:
            followed_user = User.objects.get(id=followed_user_id)
        except followed_user.DoesNotExist:
            return Response("The followed user does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if current_user.__eq__(followed_user):
            return Response("You cannot UnFollow yourself.", status=status.HTTP_400_BAD_REQUEST)

        if not current_user.following.filter(followeduser=followed_user, active=True).exists():
            return Response("You do not follow this user", status=status.HTTP_400_BAD_REQUEST)

        follow = current_user.following.get(followeduser=followed_user, follower=current_user)
        follow.delete()

        return Response("UnFollow successfully.", status=status.HTTP_200_OK)


class BookingViewSet(viewsets.ViewSet):
    queryset = Booking.objects.filter(active=True).all()
    serializer_class = serializers.BookingSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    @swagger_auto_schema(
        operation_description="Create Booking",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=True,
                default="Bearer your_token_here"
            ),
            openapi.Parameter(
                name="post",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_INTEGER,
                description="Post Id",
                required=True
            ),
        ],
        responses={
            201: openapi.Response(
                description="Booking created successfully",
                schema=serializers.BookingSerializer
            ),
            400: openapi.Response(
                description="Bad request"
            )
        }
    )
    @action(methods=['post'], url_name='create-booking', detail=False)
    def create_booking(self, request):
        serializer = self.serializer_class(data={
            'user': request.user.id,
            'post': request.data.get('post'),
            'status': 0
        })
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete Booking",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Booking Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['post'], url_path='delete-booking', detail=False)
    def delete_booking(self, request):
        pk = request.data.get('pk')

        try:
            booking = self.queryset.get(id=pk)
        except Booking.DoesNotExist:
            return Response("This Booking does not exist.", status=status.HTTP_404_NOT_FOUND)

        if booking.status == 1:
            return Response("Your schedule has been accepted. You cannot delete", status=status.HTTP_404_NOT_FOUND)

        booking.delete()

        return Response("Delete booking successfully.", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="List Booking Not Accept",
        manual_parameters=[
            openapi.Parameter(
                name="Authorization",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                description="Bearer token",
                required=True,
                default="Bearer your_token_here"
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
                schema=serializers.BookingSerializer
            ),
            404: openapi.Response(
                description="Not Found"
            )
        }
    )
    @action(methods=['get'], url_name='list-booking-not-accept', detail=False)
    def list_booking_not_accept(self, request):
        user = request.user
        bookings = self.queryset.filter(status=0, post__user=user, post__status=1).all()

        if not bookings.exists():
            return Response("The bookings do not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.BookingSerializerShow(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Accept Booking",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Booking Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            )
        }
    )
    @action(methods=['patch'], detail=False, url_path='accept-booking')
    def accept_booking(self, request):
        pk = request.data.get('pk')

        try:
            booking = self.queryset.get(id=pk)
        except Booking.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        if booking.status != 0:
            return Response("This post has been accepted.", status=status.HTTP_400_BAD_REQUEST)

        self.serializer_class().accept_booking(booking)
        booking.refresh_from_db()

        return Response("Accept successfully", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Not Accept Booking",
        manual_parameters=[
            openapi.Parameter(
                name="pk",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_NUMBER,
                description="Booking Id",
                required=True,
            )
        ],
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['patch'], detail=False, url_path='not-accept-booking')
    def not_accept_post(self, request):
        pk = request.data.get('pk')

        try:
            booking = self.queryset.get(id=pk)
        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        if booking.status == 0:
            return Response("This booking has been not accepted.", status=status.HTTP_400_BAD_REQUEST)

        self.serializer_class().unaccept_booking(booking)
        booking.refresh_from_db()

        return Response("Not Accept successfully", status=status.HTTP_200_OK)

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("address")
        if q:
            queries = queries.filter(house__address__icontains=q)
        return queries


class RoleViewSet(viewsets.ViewSet):
    # queryset = Role.objects.all()
    queryset = Role.objects.exclude(rolename='Admin')
    serializer_class = serializers.RoleSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
