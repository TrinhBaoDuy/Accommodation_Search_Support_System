
import os
import random
from datetime import timedelta
import django

# Thiết lập môi trường Django
from django.contrib.auth.hashers import make_password
from django.db.models import Exists
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASSS.settings')
django.setup()


from ASSSs.models import *

def extract_location(topic):
    extracted_location = topic[topic.index('Quan'):]

    return extracted_location

def load_data():
    genders = [1, 2, 3]
    fake = Faker()
    so = 10
    for i in range(so):
        gender_user = random.choice(genders)
        gender_host = random.choice(genders)
        first_name_user = fake.first_name()
        last_name_user = fake.last_name()
        first_name_host = fake.first_name()
        last_name_host = fake.last_name()
        email_user = fake.email()
        email_host = fake.email()
        address_user = fake.address()
        address_host = fake.address()
        dob_user = fake.date_of_birth(minimum_age=18, maximum_age=90)
        dob_host = fake.date_of_birth(minimum_age=18, maximum_age=90)
        phone_number_user = '0826523430'
        phone_number_host = '0388853371'

        user_data = {
            'username': 'user'+str(i+20),
            'password': make_password('123'),
            'role': Role.objects.get(rolename='User'),
            'gender': gender_user,
            'first_name': first_name_user,
            'last_name': last_name_user,
            'email': email_user,
            'address': address_user,
            'dob': dob_user,
            'phonenumber': phone_number_user
        }

        host_data = {
            'username': 'host'+str(i+20),
            'password': make_password('123'),
            'role': Role.objects.get(rolename='Host'),
            'gender': gender_host,
            'first_name': first_name_host,
            'last_name': last_name_host,
            'email': email_host,
            'address': address_host,
            'dob': dob_host,
            'phonenumber': phone_number_host
        }

        # user = User.objects.create(**user_data)
        # host = User.objects.create(**host_data)

    min_follows = 5  # Số lượng mối quan hệ "follow" tối thiểu
    max_follows = 30  # Số lượng mối quan hệ "follow" tối đa

    hosts = User.objects.filter(role__rolename="Host").all()
    users = User.objects.filter(role__rolename="User").all()
    for h in hosts:
        num_follows = random.randint(min_follows, max_follows)
        for _ in range(num_follows):
            followed_user = random.choice(users)
            # Follow.objects.create(follower=followed_user, followeduser=h)


    addresses = ['Quan 7', 'Quan 6', 'Quan 5', 'Quan 4', 'Quan Go Vap', 'Quan Binh Thanh']
    prices = [1200000, 21000000, 3000000, 35000000, 1400000, 1800000, 5000000, 1500000]
    quantities = [1, 2, 3, 4]
    acreages = [12, 30, 25, 40, 32, 13, 16, 18]
    houses = []
    for _ in range(20):
        random_address = random.choice(addresses)
        random_price = random.choice(prices)
        random_quantity = random.choice(quantities)
        random_acreage = random.choice(acreages)

        house_data = {
            'address': random_address,
            'price': random_price,
            'quantity': random_quantity,
            'acreage': random_acreage,
        }

        # house = House.objects.create(**house_data)
        # house.save()
        # houses.append(house)


from django.utils import timezone

def creatr_post():
    topics = ['Nha Tro Quan 7', 'Nha Tro Quan 6', 'Nha Tro Quan 5', 'Nha Tro Quan 4', 'Nha Tro Quan Go Vap', 'Nha Tro Quan Binh Thanh']
    describes = ['Hha tro rong rai, co bang cong, wifi mien phi', 'Nha tro co cho nuoi dong vat, co ham giu xe, an ninh', 'Nha tro gan cho, gan cac truong dai goc va san bay', 'Nha tro rong rai, co gac, co cho nau an va noi that day du chi can don vao o']
    statuses = [0, 1]  # Example status values
    posts = []

    for _ in range(20):

        random_topic = random.choice(topics)
        random_describe = random.choice(describes)
        random_status = random.choice(statuses)
        random_posting_date = timezone.now() - timedelta(days=random.randint(1, 30))
        random_expiration_date = random_posting_date + timedelta(days=random.randint(1, 7))
        houses = House.objects.filter(address__contains=extract_location(random_topic)).all()
        print(houses)
        post_data = {
            'topic': random_topic,
            'describe': random_describe,
            'postingdate': random_posting_date,
            'expirationdate': random_expiration_date,
            'status': random_status,
            'house': random.choice(houses),
            'user': random.choice(User.objects.filter(role__rolename="Host").all()),
            'discount': Discount.objects.get(pk=1),
            'postingprice': PostingPrice.objects.get(pk=1)
        }
        post = Post.objects.create(**post_data)
        post.save()


def create_booking():
    users = User.objects.filter(role__rolename="User", active=True).all()
    posts = Post.objects.filter(active=True, status=1).all()
    statuses = [0, 1]

    for _ in range(5):

        random_user = random.choice(users)
        random_posts = random.choice(posts)
        random_status = random.choice(statuses)

        booking_data = {
            'user': random_user,
            # 'post': random_posts,
            'post': Post.objects.get(pk=40),
            # 'status': random_status,
            'status': 1,
        }
        booking = Booking.objects.create(**booking_data)
        booking.save()


def create_comment():
    users = User.objects.filter(role__rolename="User", active=True).all()
    posts = Post.objects.filter(active=True, status=1).all()
    fake = Faker()
    parentcomments = [None]

    for _ in range(10):

        random_user = random.choice(users)
        random_posts = random.choice(posts)
        random_value = fake.text()
        random_parent = random.choice(parentcomments)

        comment_data = {
            'user': random_user,
            'post': random_posts,
            'value': random_value,
            'parentcomment': random_parent,
        }
        comment = Comment.objects.create(**comment_data)
        comment.save()
        # parentcomments.append(comment)


def create_typepayment():
    data = ['Cash', 'PayPal', 'Card']
    for i in data:
        TypePayment.objects.create(name=i)


def create_payment():
    typepayments = TypePayment.objects.filter(active=True).all()
    # bookings = Booking.objects.filter(active=True, status=1).all()
    bookings = Booking.objects.filter(active=True, status=1, post__id=40).all()
    for _ in range(5):

        random_booking = random.choice(bookings)
        total = random_booking.post.house.price + random_booking.post.postingprice.value
        # print(random_booking)
        # print(total)
        random_type = random.choice(typepayments)

        payment_data = {
            'booking': random_booking,
            'total': total,
            'typepayment': random_type,
        }
        payment = Payment.objects.create(**payment_data)
        payment.save()


def create_rating():
    # point = [1,2,3,4,5]
    point = [5]
    # payment_bookings = Payment.objects.all()
    payment_bookings = Payment.objects.filter(booking__post__id=40).all()
    bookings = [payment.booking for payment in payment_bookings]
    fake = Faker()
    for _ in range(10):

        random_point = random.choice(point)
        random_booking = random.choice(bookings)
        # print(random_booking)
        # print(total)
        value = fake.text()

        rating_data = {
            'point': random_point,
            'booking': random_booking,
            'value': value,
        }
        rating = Rating.objects.create(**rating_data)
        rating.save()


if __name__ == '__main__':
    # creatr_post()
    # create_booking()
    # create_payment()
    create_rating()
    print('Data loaded successfully.')
