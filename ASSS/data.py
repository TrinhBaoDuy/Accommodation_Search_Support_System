import os
import django

# Thiết lập môi trường Django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ASSS.settings')
django.setup()


from ASSSs.models import Role, User, Follow


def load_data():
    roles = ['Admin', 'Host', 'User']
    for role in roles:
        Role.objects.get_or_create(rolename=role)

    users_data = [
        {
            'username': 'admin',
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'phonenumber': '123456789',
            'dob': '1990-01-01',
            'address': '123 Main St',
            'role': Role.objects.get(rolename='Admin'),
            'password': make_password('123')
        },
        {
            'username': 'jane_smith',
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'phonenumber': '987654321',
            'dob': '1995-05-10',
            'address': '456 Elm St',
            'role': Role.objects.get(rolename='User'),
            'password': make_password('123')
        },
        {
            'username': 'host1',
            'first_name': 'Host',
            'last_name': 'One',
            'email': 'host1@example.com',
            'phonenumber': '111111111',
            'dob': '1990-01-01',
            'address': '123 Main St',
            'role': Role.objects.get(rolename='Host'),
            'password': make_password('123')
        },
        {
            'username': 'host2',
            'first_name': 'Host',
            'last_name': 'Two',
            'email': 'host2@example.com',
            'phonenumber': '222222222',
            'dob': '1990-02-02',
            'address': '456 Elm St',
            'role': Role.objects.get(rolename='Host'),
            'password': make_password('123')
        },
        {
            'username': 'host3',
            'first_name': 'Host',
            'last_name': 'Three',
            'email': 'host3@example.com',
            'phonenumber': '333333333',
            'dob': '1990-03-03',
            'address': '789 Oak St',
            'role': Role.objects.get(rolename='Host'),
            'password': make_password('123')
        },
        {
            'username': 'user1',
            'first_name': 'User',
            'last_name': 'One',
            'email': 'user1@example.com',
            'phonenumber': '444444444',
            'dob': '1995-01-01',
            'address': '123 Main St',
            'role': Role.objects.get(rolename='User'),
            'password': make_password('123')
        },
        {
            'username': 'user2',
            'first_name': 'User',
            'last_name': 'Two',
            'email': 'user2@example.com',
            'phonenumber': '555555555',
            'dob': '1995-02-02',
            'address': '456 Elm St',
            'role': Role.objects.get(rolename='User'),
            'password': make_password('123')
        },
    ]

    account_data_host =[]
    account_data_user =[]
    for user_data in users_data:
        user, created = User.objects.get_or_create(**user_data)
        if user.role_id == 2:
            account_data_host.append(user.id)
            print("host: " + str(user.id))
        elif user.role_id == 3:
            account_data_user.append(user.id)
            print("user: " + str(user.id))


    follow_data = [
        {
            'follower': User.objects.get(id=account_data_user[0]),
            'followeduser': User.objects.get(id=account_data_host[0])
        },
        {
            'follower': User.objects.get(id=account_data_user[1]),
            'followeduser': User.objects.get(id=account_data_host[1])
        },
        {
            'follower': User.objects.get(id=account_data_user[0]),
            'followeduser': User.objects.get(id=account_data_host[1])
        },
        {
            'follower': User.objects.get(id=account_data_host[2]),
            'followeduser': User.objects.get(id=account_data_user[0])
        },

    ]

    for data in follow_data:
        follow = Follow.objects.create(**data)


if __name__ == '__main__':
    load_data()
    print('Data loaded successfully.')
