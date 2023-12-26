from .models import House, User, Role
from django.db.models import Count


def load_houses(params={}):
    h = House.objects.all()

    kw = params.get('kw')
    if kw:
        h = h.filter(id=kw)

    return h


def count_image_by_house():
    return House.objects.annotate(count_images=Count('images__id')).values("id", "address", "count_images").order_by('-count_images')


def count_user_by_role():
    return Role.objects.exclude(rolename='ADMIN').annotate(count_users=Count('users')).values("rolename", "count_users").order_by('count_users')
