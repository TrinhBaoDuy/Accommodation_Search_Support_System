from django.urls import path, include
from rest_framework import routers
from ASSSs import views

router = routers.DefaultRouter()
router.register('houses', views.HouseViewSet, basename='houses')
router.register('image', views.ImageViewSet, basename='image')
urlpatterns = [
    path('', include(router.urls))
]
