import dataclasses
import datetime

from django.db.models.functions import ExtractYear, ExtractMonth
from ASSSs.models import *
from django.db.models import Count, Q, Case, When, IntegerField, Min, Avg, Sum


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


def count_infor_system():
    year = datetime.datetime.now().year
    past_year = year-1
    total_account = User.objects.filter(active=True).count()
    total_post = Post.objects.filter( active=True, created_date__year=year).count()
    list_total_price = Booking.objects.filter(active=True,created_date__year=year, status=1).all().values("post__postingprice")
    total_sum = 0
    for item in list_total_price:
        total_sum += item.get('post__postingprice')
    total_account_previous_year = User.objects.filter(created_date__year=past_year, active=True).count()
    total_account_now_year = User.objects.filter(created_date__year=year, active=True).count()
    growth_rate = ((total_account_now_year*100) / (total_account_previous_year+total_account_now_year))
    exchange_rate = 23000
    total_sum_usd = total_sum / exchange_rate
    return {
        'year': year,
        'past_year':  past_year,
        'total_account': total_account,
        'total_post': total_post,
        'total_price': "${:,.0f}".format(total_sum),
        'growth_rate': round(growth_rate)
    }


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


def count_post():
    year = datetime.datetime.now().year
    part_year = year-1
    count_post_year = Post.objects.filter(active=True,created_date__year=year).count()
    count_post_part_year = Post.objects.filter(active=True,created_date__year=part_year).count()
    return {
        'count_post_year': count_post_year,
        'count_post_part_year': count_post_part_year,
        'year': year,
        'part_year': part_year
    }


def get_year():
    year = datetime.datetime.now().year
    first_year = earliest_year = User.objects.aggregate(earliest_year=Min('created_date__year'))['earliest_year']

    year_data = []
    for y in range(year, first_year - 1, -1):
        year_data.append(y)

    return year_data


def top_hosts_post_a_lot():
    list_infor = []
    year = datetime.datetime.now().year
    top_hosts = User.objects.filter(role__rolename='Host', posts__active=True, posts__created_date__year=year).annotate(post_count=Count('posts')).order_by('-post_count')[:3]
    for u in top_hosts:
        list_posts = Post.objects.filter(user=u).all()
        count = 0
        point = 0
        for p in list_posts:
            list_booking = Booking.objects.filter(post=p).all()
            for b in list_booking:
                list_rating = Rating.objects.filter(booking=b).all()
                for r in list_rating:
                    point += r.point
                    count += 1
        if count == 0:
            count = 1
        point = point/count
        list_infor.append({'id': u.id, 'avg': point,'user':u})

    print(list_infor[0])
    return list_infor


def top_hosts_follower_a_lot():
    list_infor = []
    top_hosts = User.objects.filter(role__rolename='Host', followers__active=True).annotate(followers_number=Count('followers')).order_by('-followers_number')[:3]
    for u in top_hosts:
        list_posts = Post.objects.filter(user=u).all()
        count = 0
        point = 0
        for p in list_posts:
            list_booking = Booking.objects.filter(post=p).all()
            for b in list_booking:
                list_rating = Rating.objects.filter(booking=b).all()
                for r in list_rating:
                    point += r.point
                    count += 1
        if count == 0:
            count = 1
        point = point/count
        list_infor.append({'id': u.id, 'avg': point,'user':u})

    # print(list_infor)
    return list_infor


def load_user(params={}):
    h = User.objects.all()

    kw = params.get('kw')
    if kw:
        h = h.filter(id=kw)

    return h


def count_user_role_by_year(params={}):
    past_year = params.get('selected_year')
    print('--------------MMMMMMMMMMMMMMM--------------')
    print(past_year)
    if not past_year:
        past_year = '2020'
    current_year = datetime.datetime.now().year
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
    year = params.get('selected_year')
    print('--------------MMMMMMMMMMMMMMM--------------')
    print(year)
    if not year:
        year = datetime.datetime.now().year
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
    year = params.get('selected_year')
    print('--------------QQQQQQQQQQQQQQ--------------')
    print(year)
    if not year:
        year = datetime.datetime.now().year
    quarters = [1, 2, 3, 4]  # Danh sách các quý
    result = []
    year_params = {'selected_year': year}
    month_result = count_users_each_month_of_the_year(year_params)
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
                quarter_data['quarter'] = "Quarter "+str(month // 4 + 1)
                quarter_data['active_users_role_is_host'] += month_data['active_users_role_is_host']
                quarter_data['not_active_users_role_is_host'] += month_data['not_active_users_role_is_host']
                quarter_data['active_users_role_is_user'] += month_data['active_users_role_is_user']
                quarter_data['not_active_users_role_is_user'] += month_data['not_active_users_role_is_user']
        result.append(quarter_data)

    # print('--------------MMMMMMMMMMMMMMMMMMMMMMMM---RRRRRRRRRRRRRRRRRRRR-----------')
    # print(result)
    return result


def top_host_active():
    users = User.objects.filter(role__rolename='Host',active=True).annotate(post_count=Count('posts')).order_by('-post_count').values('id','username','first_name','last_name','avatar','gender','dob','post_count')[:8]
    info = []
    for user in users:
        p = Post.objects.filter(user__id=user['id']).count()
        l = Like.objects.filter(post__user__id=user['id']).count()
        f = Follow.objects.filter(followeduser__id=user['id']).count()
        queryset = Booking.objects.filter(post__user__id=user['id'], status=1).annotate(sum_price=Sum('post__house__price')).values('sum_price')
        sum_price = 0
        for item in queryset:
            sum_price += item['sum_price']
        user_info = {
            'user': user,
            'posts': p,
            'likes': l,
            'followers': f,
            'prices': "{:,.0f} VND".format(sum_price),
        }
        info.append(user_info)

    return info


def get_user_inactive_more_than_2m():
    current_date = datetime.datetime.now().date()
    if current_date.month > 2:
        two_months_ago = current_date.replace(month=current_date.month - 2)
    else:
        # Nếu tháng hiện tại là tháng 1, điều chỉnh năm lại thành năm trước và tháng là tháng 12
        two_months_ago = current_date.replace(year=current_date.year - 1, month=12)
    user = User.objects.filter(active=False,  deleted_date__lt=two_months_ago).all()
    count = User.objects.filter(active=False,  deleted_date__lt=two_months_ago).count()
    return {
        'user': user,
        'count': count
    }
