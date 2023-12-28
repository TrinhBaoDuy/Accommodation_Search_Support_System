import datetime

from ASSSs.models import House , Image, Post, Discount, PostingPrice, User, Follow, Booking, Role, Comment
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class HouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = House
        fields = ('id', 'address', 'acreage', 'price', 'quantity')


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'imageURL', 'house')


class ImageSerializerShow(serializers.ModelSerializer):
    house = HouseSerializer()
    class Meta:
        model = Image
        fields = '__all__'


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

    def update_avatar(self, user, new_avatar):
        user.avatar = new_avatar
        user.save()
        return user.avatar


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

    def create_or_update_follow(self, validated_data):
        follow = Follow.objects.create(**validated_data)
        follow.save()
        return follow


class FollowSerializerShow(serializers.ModelSerializer):
    follower = UserSerializer()
    followeduser = UserSerializer()
    class Meta:
        model = Follow
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'topic', 'describe', 'postingdate', 'expirationdate', 'status', 'discount', 'house', 'postingprice', 'user')

    def accept_post(self, post):
        post.status = 1
        post.save()
        return post

    def unaccept_post(self, post):
        post.status = 0
        post.save()
        return post


class PostSerializerShow(serializers.ModelSerializer):
    house = HouseSerializer()
    user = UserSerializer()
    discount = DiscountSerializer()
    postingprice = PostingPriceSerializer()
    class Meta:
        model = Post
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'status', 'post', 'user')

    def accept_booking(self, booking):
        booking.status = 1
        booking.save()
        return booking

    def unaccept_booking(self, booking):
        booking.status = 0
        booking.save()
        return booking



class BookingSerializerShow(serializers.ModelSerializer):
    post = PostSerializerShow()
    user = UserSerializer()

    class Meta:
        model = Booking
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'value', 'post', 'user', 'parentcomment')

    def create_comment(self, validated_data):
        data = validated_data.copy()
        comment = Comment.objects.create(**data)
        comment.save()
        return comment

    def change_value_comment(self,comment, value):
        comment.value = value
        comment.save()
        return comment


class CommentSerializerShow(serializers.ModelSerializer):
    user = UserSerializer()
    post = PostSerializerShow()

    class Meta:
        model = Comment
        fields = '__all__'

