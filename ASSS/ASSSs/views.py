import json
import os
from decimal import Decimal

import paypalrestsdk
import requests
from aiohttp.web_routedef import view
from django.core import mail
from django.db import transaction
from django.db.models import Count
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMultiAlternatives, EmailMessage
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action, permission_classes
from requests_oauthlib import OAuth2Session
from ASSS import settings
from ASSSs import serializers, paginators
from ASSSs import perms
from ASSSs.models import *
from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.response import Response
from twilio.rest import Client
import random
import datetime
from .filters import PostFilter, UserFilter
from django_filters.rest_framework import DjangoFilterBackend
import uuid
from django.urls import reverse
from django.http import JsonResponse


#vnpay
# def payment(request):
#     if request.method == 'POST':
#         # Process input data and build url payment
#         form = PaymentForm(request.POST)
#         if form.is_valid():
#             order_type = form.cleaned_data['order_type']
#             order_id = form.cleaned_data['order_id']
#             amount = form.cleaned_data['amount']
#             order_desc = form.cleaned_data['order_desc']
#             bank_code = form.cleaned_data['bank_code']
#             language = form.cleaned_data['language']
#             ipaddr = get_client_ip(request)
#             # Build URL Payment
#             vnp = vnpay()
#             vnp.requestData['vnp_Version'] = '2.1.0'
#             vnp.requestData['vnp_Command'] = 'pay'
#             vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
#             vnp.requestData['vnp_Amount'] = amount * 100
#             vnp.requestData['vnp_CurrCode'] = 'VND'
#             vnp.requestData['vnp_TxnRef'] = order_id
#             vnp.requestData['vnp_OrderInfo'] = order_desc
#             vnp.requestData['vnp_OrderType'] = order_type
#             # Check language, default: vn
#             if language and language != '':
#                 vnp.requestData['vnp_Locale'] = language
#             else:
#                 vnp.requestData['vnp_Locale'] = 'vn'
#                 # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
#             if bank_code and bank_code != "":
#                 vnp.requestData['vnp_BankCode'] = bank_code
#
#             vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')
#             vnp.requestData['vnp_IpAddr'] = ipaddr
#             vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
#             vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
#             print(vnpay_payment_url)
#                 return redirect(vnpay_payment_url)
#         else:
#             print("Form input not validate")
#     else:
#         return render(request, "payment.html", {"title": "Thanh toán"})


#mail
class SendMailViewSet(viewsets.ViewSet):

    def create(self,request):
        host = request.user
        email_followers = Follow.objects.filter(followeduser=host).values('follower__email', 'follower__first_name', 'follower__last_name')
        success_count = 0
        connection = mail.get_connection()
        # for follower in email_followers:
        subject = str(host.first_name + " " + host.last_name) + " có tin mới !!!"
        # tennguoigui = str(follower['follower__first_name'] + follower['follower__last_name'])
        tennguoigui = 'do coi ma'
        tennguoidangtin = str(host.first_name + " " + host.last_name)
        linkbaiviet = 'nhap'
        tieudebaiviet = 'nhap'
        from_email = "trinhbaoduy.26012019@gmail.com"
        to = "2051050075duy@ou.edu.vn"
        html_content = f"""
        <p>Xin chào {tennguoigui},</p>
        <p>Chúng tôi xin thông báo rằng bạn đang theo dõi {tennguoidangtin}. Chúng tôi vừa đăng một bài viết mới và muốn chia sẻ nó với bạn.</p>
        <p>Hãy truy cập vào <a href="{linkbaiviet}">{tieudebaiviet}</a> để đọc bài viết mới nhất của chúng tôi.</p>
        <p>Xin chân thành cảm ơn và hy vọng bạn tìm thấy nội dung bài viết hữu ích.</p>
        <p>Chúc bạn một ngày tốt lành!</p>
        <img src='https://res.cloudinary.com/dstqvlt8d/image/upload/v1704609698/ASSS-avatar/a0lpq48qktdfsozlba97.jpg'/>
        """
        msg = mail.EmailMessage(subject, html_content, from_email, [to], connection=connection)
        msg.content_subtype = "html"
        success_count = msg.send()
        if success_count == 1:
            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send email.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# paypal
class PayPalViewSet(viewsets.ViewSet):

    def list(self, request):
        context = {
            'url': settings.PAYPAL_CLIENT_ID,
            'price': 1,
            'description': 'hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh'
        }
        return render(request, 'paypal/payment.html', context)

    def paymentComplete(request):
        breakpoint()
        print('Thanh cong nghe', request.data.get("price"))
        return JsonResponse('Payment completed!', safe=False)


class GetHouse(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = House.objects.filter(active=True).all()
    serializer_class = serializers.HouseSerializer


class HouseViewSet(viewsets.ViewSet):
    queryset = House.objects.filter(active=True).all()
    serializer_class = serializers.HouseSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
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

    def list(self, request):
        queryset = self.queryset
        serializer = serializers.ImageSerializerShow(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostViewSet(viewsets.ViewSet, generics.ListAPIView , generics.RetrieveAPIView):
    queryset = Post.objects.filter(active=True).all()
    serializer_class = serializers.PostSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = PostFilter
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        filtered_queryset = self.filter_queryset(queryset)
        # queryset = self.filterset_class(self.queryset)
        serializer = serializers.PostSerializerShow(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='check_like', detail=True)
    def check_like(self, request,pk):
        user = request.user
        post = Post.objects.get(pk=pk)
        if not user or not post:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)
        check = Like.objects.get(user=user, post=post, status=True)
        if check:
            return Response(True, status=status.HTTP_200_OK)

        return Response(False, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], url_name='count_like', detail=True)
    def count_like(self, request, pk):
        try:
            post = self.queryset.get(pk=pk)

        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)

        count = Like.objects.filter(post=post).count()
        return Response(count, status=status.HTTP_200_OK)

    @action(methods=['get'], url_name='list-post-not-accepted', detail=False)
    def list_post_not_accepted(self, request):
        queryset = self.queryset.filter(status=0).all()
        serializer = serializers.PostSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='top-posts', detail=False)
    def top_posts(self, request):
        queryset = self.queryset.annotate(like_count=Count('likes')).order_by('-like_count')[:10]
        serializer = serializers.PostSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], url_name='list-post-accepted', detail=False)
    def list_post_accepted(self, request):
        queryset = self.queryset.filter(status=1).filter(postingdate__lte=datetime.datetime.now(), expirationdate__gte=datetime.datetime.now()).order_by('-postingdate').all()
        info = []
        for post in queryset:
            information = {
                'post': serializers.PostSerializerShow(post).data,
                'count': Like.objects.filter(post=post).count()
            }
            info.append(information)
        return Response(info, status=status.HTTP_200_OK)

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
            serializers.PostSerializerShow(serializer)
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
    @action(methods=['delete'], url_path='delete-post', detail=True)
    def delete_post(self, request, pk):
        try:
            post = self.queryset.get(pk=pk)
        except Post.DoesNotExist:
            return Response("This post does not exist.", status=status.HTTP_404_NOT_FOUND)
        post.delete_permanently()

        return Response("Delete post successfully.", status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='comments')
    def comment(self, request, pk):
        post = self.queryset.filter(id=pk).first()
        if not post:
            return Response(status=status.HTTP_404_NOT_FOUND)
        comments = post.comment_set.all().filter(active=True).order_by('-created_date')
        return Response(serializers.CommentSerializerShow(comments, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True).order_by('-created_date').all()
    serializer_class = serializers.CommentSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return serializers.CommentSerializerShow
        return serializers.CommentSerializer

    def get_permissions(self):
        if self.action.__eq__('destroy'):
            return [perms.CommentOwner()]
        elif self.action.__eq__('change_value_comment'):
            return [perms.CommentOwner()]
        else:
            return [permissions.IsAuthenticated()]

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

    # @action(methods=['delete'], url_path='delete-comment', detail=True)
    # def delete_comment(self, request, pk):
    #     try:
    #         comment = self.get_object()
    #     except Comment.DoesNotExist:
    #         return Response("This comment does not exist.", status=status.HTTP_404_NOT_FOUND)
    #     comment.delete_permanently()
    #     return Response("Delete comment successfully.", status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Change value Comment",
        manual_parameters=[
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
    @action(methods=['patch'], url_path='change-value-comment', detail=True)
    def change_value_comment(self, request, pk):
        value = request.data.get('value')
        try:
            comment = self.queryset.get(id=pk)

        except Comment.DoesNotExist:
            return Response("This comment does not exist.", status=status.HTTP_404_NOT_FOUND)

        if comment.active == 0:
            return Response("The comment has been deleted", status=status.HTTP_404_NOT_FOUND)

        comment.value = value
        comment.save()
        return Response("Change value comment successfully.", status=status.HTTP_200_OK)

    @action(methods=['get'], url_path='comment-rep', detail=True)
    def delete_comment(self, request, pk):
        try:
            parentComment = self.queryset.filter(parentcomment=pk).all()
        except Comment.DoesNotExist:
            return Response("This Comment does not exist.", status=status.HTTP_404_NOT_FOUND)
        serializer = serializers.CommentSerializerShow(parentComment ,many=True).data

        return Response(serializer, status=status.HTTP_200_OK)


class DiscountViewSet(viewsets.ModelViewSet):
    queryset = Discount.objects.all()
    serializer_class = serializers.DiscountSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None


class GetUserById(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = User.objects.filter(active=True).all()
    serializer_class = serializers.UserSerializerShow


class GetUserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.filter(active=True).all()
    serializer_class = serializers.UserSerializerShow
    parser_classes = [parsers.MultiPartParser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        filtered_queryset = self.filter_queryset(queryset)
        serializer = serializers.UserSerializerShow(filtered_queryset, many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='notices')
    def notices(self, request, pk):
        user = self.queryset.filter(id=pk).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        notices = Notice.objects.filter(user=user, active=True).all()
        serialized_data = serializers.NoticeSerializerShow(notices, many=True, context={'request': request}).data
        response_data = {
            'notices': serialized_data,
            'count': notices.count()
        }
        return Response(response_data, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects.filter(active=True).all()
    serializer_class = serializers.UserSerializerShow
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    def get_permissions(self):
        if self.action.__eq__('current_user') or self.action.__eq__('reset_password'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = serializers.UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Reset password",
        manual_parameters=[
            openapi.Parameter(
                name="first_name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="first_name",
                required=False
            ),
            openapi.Parameter(
                name="last_name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="last_name",
                required=False
            ),
            openapi.Parameter(
                name="email",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="email",
                required=False
            ),
            openapi.Parameter(
                name="address",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="address",
                required=False
            ),
            openapi.Parameter(
                name="dod",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="dod",
                required=False
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
    def partial_update(self, request, pk=None):
        user = User.objects.get(pk=pk)
        serializer = serializers.UserSerializerUpdate(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Delete a user by ID",
        responses={
            200: openapi.Response(
                description="User delete successfully",
                schema=serializers.UserSerializer
            ),
            404: openapi.Response(
                description="User not found"
            )
        }
    )
    @action(methods=['post'], url_name='delete', detail=True)
    def delete_user_by_id(self, request, pk=None):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user.delete(),
        return Response('Delete successfully', status=status.HTTP_200_OK)

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
        return Response(self.serializer_class(request.user).data)

    @swagger_auto_schema(
        operation_description="Get the follower",
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
                description="Successfully",
            ),
            400: openapi.Response(
                description="User does not exist",
            ),
        }
    )
    @action(methods=['get'], url_name='my_infor_count', detail=False)
    def my_infor_count(self, request):
        user = request.user,
        count_follower = Follow.objects.filter(followeduser_id=request.user.id, follower__active=True, active=True).count()
        count_following = Follow.objects.filter(follower_id=request.user.id, followeduser__active=True, active=True).count()
        count_post = Post.objects.filter(user__id=request.user.id, active=True).count()
        return Response({'count_follower': count_follower, 'count_following': count_following, 'count_post':count_post}, status=status.HTTP_200_OK)

    @action(methods=['get'], url_name='infor_count', detail=True)
    def infor_count(self, request, pk):
        try:
            user = self.queryset.get(pk=pk)
        except User.DoesNotExist:
            return Response("User does not exist",status=status.HTTP_404_NOT_FOUND)
        count_follower = Follow.objects.filter(followeduser__id=pk, follower__active=True, active=True).count()
        count_following = Follow.objects.filter(follower__id=pk, followeduser__active=True, active=True).count()
        count_post = Post.objects.filter(user__id=pk, active=True).count()
        return Response({'count_follower': count_follower, 'count_following': count_following, 'count_post': count_post}, status=status.HTTP_200_OK)

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
                type=openapi.TYPE_STRING,
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
    @action(methods=['post'], url_path='Send-OTP', detail=False)
    def send_otp(self, request):
        phone_number = request.data.get('phone_number')
        Country_Code='+84'
        # u = User.objects.get(phonenumber=phone_number).all()
        # if not u:
        #     return Response("User with this phone number does not exist.", status=status.HTTP_400_BAD_REQUEST)

        account_sid = settings.TWILLO_ACCOUNT_SID
        auth_token = settings.TWILLO_AUTH_TOKEN
        from_number = '+17247172226'
        verify_sid = settings.TWILLO_VENRIFY_SID
        verified_number = "+84388853371"
        client = Client(account_sid, auth_token)

        message_otp = client.verify.v2.services(verify_sid).verifications.create(to=verified_number, channel="sms")
        otp_code = message_otp.channel
        print(otp_code)
        if message_otp.status == "pending":
            return Response("SEND OTP OK", status=status.HTTP_200_OK)
        else:
            return Response("SEND OTP FALSE", status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Check OTP And Change password",
        manual_parameters=[
            openapi.Parameter(
                name="otp_check",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="Enter the OTP just notified in SMS",
                required=True,
            ),
            openapi.Parameter(
                name="phone_number",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                description="phone_number",
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
        phone_number = request.data.get('phone_number')
        otp_check = request.data.get('otp_check')
        new_password = request.data.get('new_password')

        if not phone_number or not otp_check:
            return Response("Viet do di ba", status=status.HTTP_400_BAD_REQUEST)

        u = User.objects.get(phonenumber=phone_number).first()
        if not u:
            return Response("User with this phone number does not exist.", status=status.HTTP_400_BAD_REQUEST)

        account_sid = settings.TWILLO_ACCOUNT_SID
        auth_token = settings.TWILLO_AUTH_TOKEN
        from_number = settings.TWILLO_PHONE_NUMBER
        verify_sid = settings.TWILLO_VENRIFY_SID
        verified_number = "+84388853371"
        client = Client(account_sid, auth_token)

        check_otp = client.verify.services(verify_sid).verification_checks.create(to=verified_number, code=otp_check)

        if check_otp.status == "approved":
            serializers.UserSerializer.chang_pass(u, new_password)
            return Response("Password reset successful.", status=status.HTTP_200_OK)
        else:
            return Response("OTP Wrong . Enter your OTP again", status=status.HTTP_400_BAD_REQUEST)



    @swagger_auto_schema(
        operation_description="Upgrade Account",
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
                description="successfully",
                schema=serializers.UserSerializer
            ),
            400: openapi.Response(
                description="Bad request"
            )
        }
    )
    @action(methods=['post'], url_name='upgrade-account-send-OTP', detail=False)
    def upgrade_account_send_OTP(self, request):
        user = request.user
        print(int(user.phonenumber))
        if user.role.id == 2:
            return Response("Your Account did Upgrade", status=status.HTTP_400_BAD_REQUEST)

        phone_number = int(user.phonenumber)
        Country_Code='+84'

        account_sid = settings.TWILLO_ACCOUNT_SID
        auth_token = settings.TWILLO_AUTH_TOKEN
        from_number = settings.TWILLO_PHONE_NUMBER
        verify_sid = settings.TWILLO_VENRIFY_SID
        verified_number = "+84388853371"
        client = Client(account_sid, auth_token)

        message_otp = client.verify.v2.services(verify_sid).verifications.create(to=verified_number, channel="sms")
        if message_otp.status == "pending":
            return Response("SEND OTP OK", status=status.HTTP_200_OK)
        else:
            return Response("SEND OTP FALSE", status=status.HTTP_400_BAD_REQUEST)


    @swagger_auto_schema(
        operation_description="Check OTP And Change password",
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
                name="otp_check",
                in_=openapi.TYPE_STRING,
                type=openapi.TYPE_NUMBER,
                description="Enter the OTP just notified in SMS",
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
    @action(methods=['post'], url_path='check-OTP-upgrade-account', detail=False)
    def check_OTP_upgrade_account(self, request):
        otp_check = request.data.get('otp_check')
        user = request.user
        phonenumbers = str(int(user.phonenumber))

        account_sid = settings.TWILLO_ACCOUNT_SID
        auth_token = settings.TWILLO_AUTH_TOKEN
        from_number = settings.TWILLO_PHONE_NUMBER
        verify_sid = settings.TWILLO_VENRIFY_SID
        verified_number = "+84388853371"

        client = Client(account_sid, auth_token)

        check_otp = client.verify.services(verify_sid).verification_checks.create(to=verified_number, code=otp_check)

        if check_otp.status == "approved":
            user.role = 2
            user.save()
            return Response("Upgrade Account successful.", status=status.HTTP_200_OK)
        else:
            return Response("Check OTP False", status=status.HTTP_400_BAD_REQUEST)


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
    @action(methods=['patch'], detail=False)
    def update_avatar(self, request):
        user = request.user
        new_avatar = request.FILES.get('avatar')

        if not new_avatar:
            return Response("Avatar is required.", status=status.HTTP_400_BAD_REQUEST)
        else:
            # upload_data = cloudinary.uploader.upload(new_avatar)
            # avatar = upload_data['url']
            user.avatar = new_avatar
            user.save()
            return Response(serializers.UserSerializerShow(user).data, status=status.HTTP_200_OK)


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
        return Response(serializers.CommentSerializer(posts, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class FollowViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Follow.objects.filter(active=True).all()
    serializer_class = serializers.FollowSerializer
    pagination_class = paginators.ASSSPaginator
    parser_classes = [parsers.MultiPartParser]
    # swagger_schema = None

    @action(methods=['get'], detail=True, url_path='check')
    def check(self, request, pk):
        current_user = request.user
        user = self.get_object()
        check = self.queryset.filter(followeduser=user, follower=current_user)
        if check.exists():
            return Response({'data': True})
        else:
            return Response({'data': False})

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

    @action(methods=['get'], detail=True, url_path='followeduser')
    def followeduser(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            followed_users = self.queryset.filter(follower=user, followeduser__active=True).all()
            if followed_users:
                serializer = serializers.FollowSerializerShow(followed_users, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("User has no followed users", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)

    @action(methods=['get'], detail=True, url_path='follower')
    def follower(self, request, pk):
        user = User.objects.get(pk=pk)
        if user:
            follower = self.queryset.filter(followeduser=user, follower__active=True).all()
            if follower:
                serializer = serializers.FollowSerializerShow(follower, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response("User has no followers", status=status.HTTP_204_NO_CONTENT)
        else:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


    @swagger_auto_schema(
        operation_description="Follow",
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
    @action(methods=['post'], url_path='create-or-delete-follow', detail=False)
    def create_or_delete_follow(self, request):
        current_user = request.user
        followed_user_id = request.data.get('followed_user')

        followed_user = User.objects.get(id=followed_user_id)
        if not followed_user:
            return Response("The followed user does not exist.", status=status.HTTP_400_BAD_REQUEST)

        if current_user.__eq__(followed_user):
            return Response("You cannot follow yourself.", status=status.HTTP_400_BAD_REQUEST)

        follow, created = Follow.objects.update_or_create(follower=current_user, followeduser=followed_user)
        if not created:
            follow.status = False
            follow.delete_permanently()
            return Response("Un Follow", status=status.HTTP_204_NO_CONTENT)

        return Response("Follow", status=status.HTTP_201_CREATED)

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


class TypePaymentViewSet(viewsets.ViewSet):
    queryset = TypePayment.objects.all()
    serializer_class = serializers.TypePaymentSerializerShow
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class PaymentViewSet(viewsets.ViewSet):
    queryset = Payment.objects.filter(active=True).all()
    serializer_class = serializers.PaymentSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None

    @swagger_auto_schema(
        operation_description="List Payment History",
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
    @action(methods=['get'], url_name='list-payment-of-user', detail=False)
    def list_payment_of_user(self, request):
        user = request.user
        payments = self.queryset.filter(booking__user=user).all()

        if not payments:
            return Response("The payments do not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.PaymentSerializerShow(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="List Payment History",
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
    @action(methods=['get'], url_name='list-payment-of-host', detail=False)
    def list_payment_of_host(self, request):
        user = request.user
        payments = self.queryset.filter(booking__post__user=user).all()

        if not payments:
            return Response("The payments do not exist.", status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.PaymentSerializerShow(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create Payment",
        request_body=serializer_class,
        responses={
            200: openapi.Response(
                description="Successfully",
            ),
            400: openapi.Response(
                description="Bad request",
            ),
        }
    )
    @action(methods=['post'], detail=False, url_path='create-payment')
    def create_payment(self, request):

        booking_id = request.data.get('booking')
        type_payment = request.data.get('typepayment')

        booking = Booking.objects.filter(id=booking_id).first()
        typepayment = TypePayment.objects.filter(id=type_payment).first()

        if not typepayment:
            return Response("This Type Payment does not exist.", status=status.HTTP_404_NOT_FOUND)

        if not booking:
            return Response("This Booking does not exist.", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response("Created successfully.", status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ViewSet):
    queryset = Rating.objects.filter(active=True).all()
    serializer_class = serializers.RatingSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        rating = self.queryset.filter(pk=pk).first()
        serializer = self.serializer_class(rating)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='get-rating-of-id-user')
    def get_rating_of_id_user(self, request, pk=None):
        rating = self.queryset.filter(booking__post__user__id=pk).all()
        serializer = serializers.RatingSerializerShow(rating,many=True)
        return Response(serializer.data)

    @action(methods=['get'], detail=True, url_path='get-stars-of-id-user')
    def get_stars_of_id_user(self, request, pk=None):
        rating = self.queryset.filter(booking__post__user__id=pk).all()
        sum = 0
        count = 0
        for ra in rating:
            sum += ra.point
            count += 1
        if count == 0:
            count = 1
        avg = sum/count
        serializer = serializers.RatingSerializerShow(rating, many=True)
        return Response({'avg': round(avg), 'rating': serializer.data}, status=status.HTTP_200_OK)


class PushPostViewSet(viewsets.ViewSet):
    # swagger_schema = None

    def create(self, request):
        user = request.user
        if isinstance(user, User):
            print(user.id)
        list_host = User.objects.filter(role_id=2).all()
        if user:
            if user not in list_host:
                post_data = {
                    'topic': request.data.get("topic"),
                    'describe': request.data.get("describe"),
                    'postingdate': datetime.datetime.now(),
                    'expirationdate': datetime.datetime.now() + datetime.timedelta(days=365),
                    # 'postingdate': '2024-01-10',
                    # 'expirationdate': '2024-01-20',
                    'status': 1,
                    'house': None,
                    'user': User.objects.get(pk=user.id),
                    'discount': None,
                    'postingprice': None,
                }
                post = Post.objects.create(**post_data)
                post.save()
                print(post)
                # breakpoint()
                return Response(serializers.PostSerializerShow(post).data, status=status.HTTP_200_OK)

            address = request.data.get("address")
            acreage = request.data.get("acreage")
            price = request.data.get("price")
            quantity = request.data.get("quantity")
            if not address or not acreage or not quantity or not price:
                return Response("Info house not found", status=status.HTTP_404_NOT_FOUND)

            house = House.objects.create(address=address, acreage=acreage, price=price, quantity=quantity)
            house.save()

            if house:
                print(house)
                images = request.FILES.getlist('images')
                id_image = []
                if not images:
                    house.delete_permanently()
                    return Response("Image not found", status=status.HTTP_404_NOT_FOUND)
                for image in images:
                    img = Image.objects.create(house=house, imageURL=image)
                    img.save()
                    id_image.append(img.id)
                post_data = {
                    'topic': request.data.get("topic"),
                    'describe': request.data.get("describe"),
                    'postingdate': request.data.get("postingdate"),
                    'expirationdate': request.data.get("expirationdate"),
                    # 'postingdate': '2024-01-10',
                    # 'expirationdate': '2024-01-20',
                    'status': 0,
                    'house': House.objects.get(pk=house.id),
                    'user': User.objects.get(pk=user.id),
                    'discount': Discount.objects.get(pk=request.data.get("discount")),
                    'postingprice': request.data.get("postingprice"),
                }
                check = True
                for key, value in post_data.items():
                    if value is None:
                        check = False
                        # breakpoint()
                        return Response(f"Missing value for field {key}", status=status.HTTP_400_BAD_REQUEST)
                # breakpoint()
                if check.__eq__(False):
                    house.delete_permanently()
                    for pk in id_image:
                        Image.objects.get(pk=pk).delete_permanently()
                # breakpoint()
                post = Post.objects.create(**post_data)
                post.save()
                print(post)
                # breakpoint()
                return Response(serializers.PostSerializerShow(post).data, status=status.HTTP_200_OK)
            else:
                return Response("Info house not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("User not found", status=status.HTTP_404_NOT_FOUND)


class LikeViewSet(viewsets.ViewSet):
    queryset = Like.objects.filter(active=True).all()
    serializer_class = serializers.LikeSerializer
    pagination_class = paginators.ASSSPaginator
    # swagger_schema = None

    def list(self, request):
        queryset = self.queryset
        serializer = serializers.LikeSerializerShow(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['post'], url_name='create_or_delete_like', detail=False)
    def create_or_delete_like(self, request):
        user_id = request.data.get('user_id')
        post_id = request.data.get('post_id')

        user = User.objects.get(pk=user_id)
        post = Post.objects.get(pk=post_id)

        if not user or not post:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)

        like, created = Like.objects.update_or_create(user=user, post=post, defaults={'status': True})
        if not created:
            like.status = False
            like.delete_permanently()
            return Response("Un Like", status=status.HTTP_204_NO_CONTENT)

        return Response("Like", status=status.HTTP_201_CREATED)

    # @swagger_auto_schema(
    #     operation_description="Check Like",
    #     manual_parameters=[
    #         openapi.Parameter(
    #             name="Authorization",
    #             in_=openapi.IN_HEADER,
    #             type=openapi.TYPE_STRING,
    #             description="Bearer token",
    #             required=True,
    #             default="Bearer your_token_here"
    #         ),
    #         openapi.Parameter(
    #             name="post_id",
    #             in_=openapi.IN_FORM,
    #             type=openapi.TYPE_INTEGER,
    #             description="post_id",
    #             required=True,
    #         )
    #     ],
    #     responses={
    #         200: openapi.Response(
    #             description="Successfully",
    #         ),
    #         404: openapi.Response(
    #             description="Not Found"
    #         )
    #     }
    # )
    @action(methods=['get'], url_name='check_like', detail=False)
    def check_like(self, request):
        user = request.user
        post_id = request.data.get('post_id')

        post = Post.objects.get(pk=post_id)

        if not user or not post:
            return Response("Not Found", status=status.HTTP_404_NOT_FOUND)

        try:
            check = Like.objects.get(user=user, post=post, status=True)

        except Like.DoesNotExist:
            return Response(False, status=status.HTTP_204_NO_CONTENT)

        return Response(True, status=status.HTTP_200_OK)


class NoticeViewSet(viewsets.ViewSet,):
    queryset = Notice.objects.filter(active=True).all()
    serializer_class = serializers.NoticeSerializer
    pagination_class = paginators.ASSSPaginator

    def list(self, request):
        queryset = self.queryset
        serializer = serializers.NoticeSerializerShow(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        post_id = request.data.get('post_id')
        post = Post.objects.get(pk=post_id, active=True)
        host = post.user
        followers = Follow.objects.filter(followeduser=host, follower__active=True).all()
        with transaction.atomic():  #dam bao duy nhat
            for follower in followers:
                user = follower.follower
                notice = Notice.objects.create(post=post, user=user)
        return Response(status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        notice = Notice.objects.get(pk=pk)
        notice.delete_permanently()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        notice = Notice.objects.get(pk=pk)
        notice.status = True
        notice.save()
        return Response(status=status.HTTP_200_OK)

