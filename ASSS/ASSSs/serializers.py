import datetime

from ASSSs.models import House , Image, Post, Discount, PostingPrice, User, Follow, Booking, Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        filter= '__all_'


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
        fields = ('id', 'username', 'password', 'avatar', 'first_name', 'last_name', 'email', 'phonenumber', 'dob', 'address', 'role' )
        extra_kwargs = {
                'password': {
                    'write_only': True
                }
            }

    def create_user(self, validated_data):
        data = validated_data.copy()
        user = User.objects.create(**data)
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create_or_update_follow(self, validated_data):
        follow = Follow.objects.create(**validated_data)
        follow.save()
        return follow


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


