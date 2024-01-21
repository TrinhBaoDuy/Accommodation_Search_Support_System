from django.urls import path, include
from rest_framework import routers
from ASSSs import views
from django.urls import path

router = routers.DefaultRouter()
router.register('houses', views.HouseViewSet, basename='houses')
router.register('house', views.GetHouse, basename='house')
router.register('images', views.ImageViewSet, basename='images')
router.register('posts', views.PostViewSet, basename='posts')
router.register('users', views.UserViewSet, basename='users')
router.register('discounts', views.DiscountViewSet, basename='discounts')
router.register('bookings', views.BookingViewSet, basename='bookings')
router.register('follows', views.FollowViewSet, basename='follows')
router.register('roles', views.RoleViewSet, basename='roles')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('typepayments', views.TypePaymentViewSet, basename='typepayments')
router.register('payments', views.PaymentViewSet, basename='payments')
router.register('ratings', views.RatingViewSet, basename='ratings')
router.register('push_post', views.PushPostViewSet, basename='push_post')
router.register('users', views.GetUserViewSet, basename='users')
router.register('user', views.GetUserById, basename='user')
router.register('likes', views.LikeViewSet, basename='likes')
router.register('paypal', views.PayPalViewSet, basename='paypal')
router.register('send_mail', views.SendMailViewSet, basename='send_mail')
router.register('notices', views.NoticeViewSet, basename='notices')
urlpatterns = [
    path('', include(router.urls)),
    path('complete/', views.PayPalViewSet.paymentComplete, name="complete"),
]
