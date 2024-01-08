import django_filters
from .models import *


class PostFilter(django_filters.FilterSet):
    postingdate = django_filters.DateFilter(lookup_expr='date', label='Posting Date')
    expirationdate = django_filters.DateFilter(lookup_expr='date', label='Expiration Date')
    house__address = django_filters.CharFilter(lookup_expr='icontains', label='House Address')
    user__username = django_filters.CharFilter(lookup_expr='icontains', label='Username')
    discount__name = django_filters.CharFilter(lookup_expr='icontains', label='Discount Name')

    class Meta:
        model = Post
        fields = fields = ['postingdate', 'expirationdate', 'house__address', 'user__username', 'discount__name']


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains', label='Username')

    class Meta:
        model = User
        fields = ['username']
