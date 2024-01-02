import datetime

from django.db.models.functions import ExtractYear, ExtractMonth
from .models import House, User, Role
from django.db.models import Count, Q, Case, When, IntegerField


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


def count_host():
    total_hosts = User.objects.filter(role__rolename='Host').count()
    active_hosts = User.objects.filter(role__rolename='Host', active=True).count()
    not_active_hosts = total_hosts - active_hosts
    active_percentage = (active_hosts / total_hosts) * 100 if total_hosts > 0 else 0

    return {
        'total_hosts': total_hosts,
        'active_hosts': active_hosts,
        'not_active_hosts': not_active_hosts,
        'active_percentage': round(active_percentage)
    }


def count_user():
    total_users = User.objects.filter(role__rolename='User').count()
    active_users = User.objects.filter(role__rolename='User', active=True).count()
    not_active_users = total_users - active_users
    active_percentage = (active_users / total_users) * 100 if total_users > 0 else 0

    return {
        'total_users': total_users,
        'active_users': active_users,
        'not_active_users': not_active_users,
        'active_percentage': round(active_percentage)
    }


def load_user(params={}):
    h = User.objects.all()

    kw = params.get('kw')
    if kw:
        h = h.filter(id=kw)

    return h


def count_user_role_by_year(params={}):
    current_year = datetime.datetime.now().year
    past_year = '2020'
    all_years = list(range(int(past_year), int(current_year) + 1))

    user_count_by_role_and_year = (
        User.objects.filter(
            created_date__year__gte=past_year,
            created_date__year__lte=current_year
        )
        .annotate(year=ExtractYear('created_date'))
        .values("year")
        .annotate(
            active_users_role_is_host=Count(Case(When(active=True, role__rolename='Host', then=1), output_field=IntegerField())),
            not_active_users_role_is_host=Count(Case(When(active=False, role__rolename='Host', then=1), output_field=IntegerField())),
            active_users_role_is_user=Count(Case(When(active=True, role__rolename='User', then=1), output_field=IntegerField())),
            not_active_users_role_is_user=Count(Case(When(active=False, role__rolename='User', then=1), output_field=IntegerField()))
        )
        .order_by("year")
    )
    result = []
    for year in all_years:
        year_data = next((data for data in user_count_by_role_and_year if data['year'] == year), None)
        if year_data is None:
            year_data = {
                'year': year,
                'active_users_role_is_host': 0,
                'not_active_users_role_is_host': 0,
                'active_users_role_is_user': 0,
                'not_active_users_role_is_user': 0
            }
        result.append(year_data)

    return result


def count_users_each_month_of_the_year(params={}):
    # year = params.get('year')
    year = '2024'
    months = range(1, 13)
    user_count_by_role_and_year = (
        User.objects.filter(created_date__year=year)
        .annotate(month=ExtractMonth('created_date'))
        .values("month")
        .annotate(
            active_users_role_is_host=Count(Case(When(active=True, role__rolename='Host', then=1), output_field=IntegerField())),
            not_active_users_role_is_host=Count(Case(When(active=False, role__rolename='Host', then=1), output_field=IntegerField())),
            active_users_role_is_user=Count(Case(When(active=True, role__rolename='User', then=1), output_field=IntegerField())),
            not_active_users_role_is_user=Count(Case(When(active=False, role__rolename='User', then=1), output_field=IntegerField()))
        )
        .order_by("month")
    )
    result = []
    for month in months:
        month_data = next((item for item in user_count_by_role_and_year if item['month'] == month), None)
        if month_data is None:
            month_data = {
                'month': month,
                'active_users_role_is_host': 0,
                'not_active_users_role_is_host': 0,
                'active_users_role_is_user': 0,
                'not_active_users_role_is_user': 0
            }
        result.append(month_data)

    return result


def count_users_each_quarter_of_the_year(params={}):
    # year = params.get('year')
    year = '2023'
    quarters = [1, 2, 3, 4]  # Danh sách các quý
    result = []
    month_params = {'year': year}
    month_result = count_users_each_month_of_the_year(month_params)
    for quarter in quarters:
        quarter_data = {
            'quarter': quarter,
            'active_users_role_is_host': 0,
            'not_active_users_role_is_host': 0,
            'active_users_role_is_user': 0,
            'not_active_users_role_is_user': 0
        }

        for month_data in month_result:
            month = month_data['month']
            if month // 4 + 1 == quarter:
                quarter_data['quarter'] = "Quý "+str(month // 4 + 1)
                quarter_data['active_users_role_is_host'] += month_data['active_users_role_is_host']
                quarter_data['not_active_users_role_is_host'] += month_data['not_active_users_role_is_host']
                quarter_data['active_users_role_is_user'] += month_data['active_users_role_is_user']
                quarter_data['not_active_users_role_is_user'] += month_data['not_active_users_role_is_user']
        result.append(quarter_data)

    return result
