from ASSSs.models import House , Image, Post, Discount, PostingPrice, User, Follow, Booking
from rest_framework import serializers


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    house = HouseSerializer()

    class Meta:
        model = Image
        fields = ('id', 'imageURL', 'house')


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'


class PostingPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostingPrice
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    house = HouseSerializer(),
    user = UserSerializer(),
    discount = DiscountSerializer(),
    postingprice = PostingPriceSerializer(),

    class Meta:
        model = Post
        fields = '__all__'


