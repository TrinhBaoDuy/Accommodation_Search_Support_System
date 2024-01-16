from django.contrib.auth.models import AbstractUser, User
from django.db import models
from django.utils import timezone
from cloudinary.models import CloudinaryField


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    deleted_date = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['-id']

    def delete(self, *args, **kwargs):
        self.active = False
        self.deleted_date = timezone.now()
        self.save()

    def delete_permanently(self):
        super().delete()


class Role(models.Model):
    rolename = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.rolename


GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)


class User(AbstractUser, BaseModel):
    phonenumber = models.FloatField(default=0)
    dob = models.DateField(null=True)
    address = models.CharField(max_length=100, null=True)
    avatar = CloudinaryField('avatar', null=True, folder="ASSS-avatar")
    role = models.ForeignKey(Role, on_delete=models.RESTRICT, related_query_name='users', null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True)

    def __str__(self):
        return f"ID: {self.id}, Name: {self.first_name} {self.last_name},Gender: {self.gender}, DOB: {self.dob}, Email: {self.email}, Address: {self.address}, Role: {self.role}"


class Follow(BaseModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    followeduser = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"Follower: {self.follower} -- Followeduser: {self.followeduser}"


class House(BaseModel):
    address = models.CharField(max_length=100, null=False)
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    acreage = models.FloatField(default=0)

    def __str__(self):
        return f"ID: {self.id}, Address: {self.address}, Price: {self.price}, Soluong: {self.quantity}nguoi/phong, Dientich: {self.acreage}m^2"


class Discount(BaseModel):
    name = models.CharField(max_length=100, null=False)
    value = models.FloatField(default=0)

    def __str__(self):
        return self.name


class Post(BaseModel):
    topic = models.CharField(max_length=100, null=False)
    describe = models.CharField(max_length=1000, null=False)
    postingdate = models.DateTimeField(null=True)
    expirationdate = models.DateTimeField(null=True)
    status = models.IntegerField()
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_query_name="posts")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="posts")
    discount = models.ForeignKey(Discount, on_delete=models.RESTRICT, related_query_name="posts")
    postingprice = models.IntegerField(null=False)

    def __str__(self):
        return f"ID: {self.id}, Topic: {self.topic}, User: {self.user}, House: {self.house}, Posting Date: {self.postingdate}, Expiration Date: {self.expirationdate}, Status: {self.status}, Discount: {self.discount}, Posting Price: {self.postingprice}"


class Image(BaseModel):
    imageURL = CloudinaryField('imageURL', null=True, folder="ASSS-house")
    house = models.ForeignKey(House, on_delete=models.CASCADE, related_query_name="images")

    def __str__(self):
        return f"House: {self.house} -- Image: {self.imageURL}"


class Comment(BaseModel):
    value = models.CharField(max_length=1000, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_query_name="comments")
    parentcomment = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_query_name="comments")

    def __str__(self):
        return f"ID: {self.id}, Value: {self.value}, User: {self.user}, Post: {self.post}"


class Booking(BaseModel):
    user = models.ForeignKey(User, on_delete=models.RESTRICT, related_query_name="bookings")
    post = models.ForeignKey(Post, on_delete=models.RESTRICT, related_query_name="bookings")
    status = models.IntegerField()

    def __str__(self):
        return f"ID: {self.id}, User: {self.user}, Post: {self.post}, Status: {self.status}"


class TypePayment(BaseModel):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"ID: {self.id}, typepayment: {self.name}"


class Payment(BaseModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_query_name="payments")
    total = models.FloatField(default=0)
    typepayment = models.ForeignKey(TypePayment, on_delete=models.SET_NULL, related_query_name="payments", null=True)

    def __str__(self):
        return f"ID: {self.id}, Booking: {self.booking},total: {self.total}, Type Payment: {self.typepayment}"


class Rating(BaseModel):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_query_name="ratings")
    point = models.IntegerField()
    value = models.CharField(max_length=1000, null=False)

    def __str__(self):
        return f"ID: {self.id}, Booking: {self.booking},Point: {self.point}, Value: {self.value}"


class Like(BaseModel):
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_query_name="likes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_query_name="likes")

    class Meta:
        unique_together = ('user', 'post')


class Notice(BaseModel):
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'post')
