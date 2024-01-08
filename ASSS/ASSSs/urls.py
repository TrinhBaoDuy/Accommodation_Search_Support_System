from django.urls import path, include
from rest_framework import routers
from ASSSs import views

router = routers.DefaultRouter()
router.register('houses', views.HouseViewSet, basename='houses')
router.register('images', views.ImageViewSet, basename='images')
router.register('posts', views.PostViewSet, basename='posts')
router.register('users', views.UserViewSet, basename='users')
router.register('discounts', views.DiscountViewSet, basename='discounts')
router.register('postingprice', views.PostingPriceViewSet, basename='postingprice')
router.register('bookings', views.BookingViewSet, basename='bookings')
router.register('follows', views.FollowViewSet, basename='follows')
router.register('roles', views.RoleViewSet, basename='roles')
router.register('comments', views.CommentViewSet, basename='comments')
router.register('typepayments', views.TypePaymentViewSet, basename='typepayments')
router.register('payments', views.PaymentViewSet, basename='payments')
router.register('ratings', views.RatingViewSet, basename='ratings')
router.register('posts', views.PushPostViewSet, basename='posts')
router.register('users', views.GetUserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls))
]
