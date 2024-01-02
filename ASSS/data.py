
import os
import random

import django

# Thiết lập môi trường Django
from django.contrib.auth.hashers import make_password
from faker import Faker
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASSS.settings')
django.setup()


from ASSSs.models import Role, User, Follow


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
            'username': 'user'+str(i+10),
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
            'username': 'host'+str(i+10),
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

        user = User.objects.create(**user_data)
        host = User.objects.create(**host_data)


if __name__ == '__main__':
    load_data()
    print('Data loaded successfully.')
