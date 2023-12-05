from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.Model):
    rolename = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.rolename


class User(AbstractUser):
    phonenumber = models.FloatField(default=0)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    avatar = models.FileField(upload_to='image-house', null=True)
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, related_query_name='users', null=True)

    def __str__(self):
        return f"ID: {self.id}, Name: {self.first_name} {self.last_name}, DOB: {self.dob}, Email: {self.email}, Address: {self.address}, Role: {self.role}"


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followeduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"Follower: {self.follower} -- Followeduser: {self.followeduser}"


class House(models.Model):
    address = models.CharField(max_length=100, null=False)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    acreage = models.FloatField(default=0)

    def __str__(self):
        return f"ID: {self.id}, Address: {self.address}, Price: {self.price}, Soluong: {self.quantity}nguoi/phong, Dientich: {self.acreage}m^2"


class Discount(models.Model):
    name = models.CharField(max_length=100, null=False)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.name


class PostingPrice(models.Model):
    value = models.FloatField(default=100000)

    def __str__(self):
        return str(self.value)


class Post(models.Model):
    topic = models.CharField(max_length=100, null=False)
    describe =models.CharField(max_length=1000, null=False)
    postingdate = models.DateTimeField(null=True)
    expirationdate = models.DateTimeField(null=True)
    status = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_query_name="posts")
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_query_name="posts")
    discount= models.ForeignKey(Discount, on_delete=models.RESTRICT, related_query_name="posts")
    postingprice = models.ForeignKey(PostingPrice, on_delete=models.RESTRICT, related_query_name="posts")

    def __str__(self):
        return f"ID: {self.id}, Topic: {self.topic}, User: {self.user}, House: {self.house}, Posting Date: {self.postingdate}, Expiration Date: {self.expirationdate}, Status: {self.status}, Discount: {self.discount}, Posting Price: {self.postingprice}"


class Image(models.Model):
    imageURL = models.FileField(upload_to='image-house')
    house = models.ForeignKey(House, on_delete=models.RESTRICT, related_query_name="images")

    def __str__(self):
        return f"House: {self.house} -- Image: {self.imageURL}"


class Comment(models.Model):
    commentdate = models.DateTimeField(auto_now_add=True, null=True)
    value = models.CharField(max_length=1000, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_query_name="comments")
    parentcomment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_query_name="comments")

    def __str__(self):
        return f"ID: {self.id}, Value: {self.value}, User: {self.user}, Post: {self.post}"


class Booking(models.Model):
    bookingdate = models.DateTimeField(auto_now_add=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="bookings")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_query_name="bookings")
    status = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, Booking Date: {self.bookingdate}, User: {self.user}, Post: {self.post}, Status: {self.status}"
