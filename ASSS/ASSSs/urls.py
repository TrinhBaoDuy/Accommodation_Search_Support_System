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
urlpatterns = [
    path('', include(router.urls))
]
