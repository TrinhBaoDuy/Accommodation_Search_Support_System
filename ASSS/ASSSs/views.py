
from django.http import Http404, HttpResponseRedirect
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from ASSSs import serializers, paginators
from ASSSs.models import House, Image, Post, Discount, PostingPrice, User, Follow, Booking
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


class HouseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = House.objects.all()
    serializer_class = serializers.HouseSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None


    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    # @permission_classes([IsAuthenticated])
    def retrieve(self, request, pk=None):
        house = self.get_object(pk)
        serializer = self.serializer_class(house)
        return Response(serializer.data)

    # @permission_classes([IsAuthenticated])
    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permission_classes([IsAuthenticated])
    def update(self, request, pk=None):
        house = self.get_object(pk)
        serializer = self.serializer_class(house, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # @permission_classes([IsAuthenticated])
    def destroy(self, request, pk=None):
        house = self.get_object(pk)
        house.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return House.objects.get(pk=pk)
        except House.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queryset = self.queryset

        address = self.request.query_params.get("address")
        if address:
            queryset = queryset.filter(address__icontains=address)

        return queryset

    @action(methods=['get'], detail=True)
    def images(self, request, pk):
        images = self.get_object().image_set.all()
        # import pdb
        # pdb.set_trace()
        return Response(serializers.ImageSerializer(images, many=True,  context={'request': request}).data,
                        status=status.HTTP_200_OK)


class ImageViewSet(viewsets.ModelViewSet, generics.ListAPIView):
    queryset = Image.objects.all()
    serializer_class = serializers.ImageSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None
    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("houseID")
        if q:
            queries = queries.filter(house__id=q)

        return queries


class PostViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = self.get_object(pk)
        serializer = self.serializer_class(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("address")
        if q:
            queries = queries.filter(house__address__icontains=q)
        return queries


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None


class PostingPriceViewSet(viewsets.ModelViewSet):
    queryset = PostingPrice.objects.all()
    serializer_class = serializers.PostingPriceSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]

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
    def create_user(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
                description="Successful operation",
                schema=serializers.UserSerializer
            )
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
    @action(methods=['post'], url_path='reset-password', detail=False)
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


class FollowViewSet(viewsets.ViewSet):
    queryset = Follow.objects.filter(active=True).all()
    serializer_class = serializers.FollowSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]

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
                schema=serializers.UserSerializer
            )
        }
    )
    @action(methods=['get'], detail=False, url_path='followers-by-current-user')
    def followers_by_current_user(self, request):
        current_user = request.user
        try:
            followers = self.queryset.filter(followeduser=current_user)
            serializer = serializers.FollowSerializer(followers, many=True)
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
            serializer = serializers.FollowSerializer(followeduser, many=True)
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



class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingSerializer
    pagination_class = paginators.ASSSPaginator
    swagger_schema = None
