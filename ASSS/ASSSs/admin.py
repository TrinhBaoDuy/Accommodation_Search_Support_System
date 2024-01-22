from django.contrib import admin
from django.shortcuts import render
from django.template.response import TemplateResponse

from . import dao
from .models import Post,House,Comment,Discount,Role,Image,Follow,Booking,User
from django.urls import path
# Register your models here.


class ASSSAdminSite(admin.AdminSite):
    site_header = 'Quan Ly He Thong'

    def get_urls(self):
        return [
                   path('ASSS-stats/', self.stats_view),
                   path('ASSS-nhap/', self.nhap)
               ] + super().get_urls()

    def stats_view(self, request):
        print(request.GET.get('selected_year', ''))
        return TemplateResponse(request, 'admin/nhap.html', {
            'stats': dao.count_image_by_house(),
            'houses': dao.load_houses(),
            'statsUser': dao.count_user_by_role(),
            'users': dao.load_user(),
            'stats_user_role_by_year': dao.count_user_role_by_year(request.GET),
            'stats_user_role_by_month': dao.count_users_each_month_of_the_year(request.GET),
            'stats_user_role_by_quarter': dao.count_users_each_quarter_of_the_year(request.GET),
            'count_host': dao.count_host(),
            'count_user': dao.count_user(),
            'count_info_sys': dao.count_infor_system(),
            'top_hosts': dao.top_hosts_post_a_lot(),
            'hot_hots': dao.top_hosts_follower_a_lot(),
            'count_post': dao.count_post(),
            'year_data': dao.get_year(),
            'top_host_active': dao.top_host_active(),
            'u_2m': dao.get_user_inactive_more_than_2m(),
            'statistics_type': request.GET.get('statistics_type', 'Statistics_month'),
            'selected_year': request.GET.get('selected_year', '2024'),
        })

    def nhap(self, request):
        return TemplateResponse(request, 'admin/stats.html', {
            'top_hosts': dao.top_hosts_post_a_lot(),
        })


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'rolename']
    search_fields = ['rolename']
    list_filter = ['id', 'rolename']

    class Media:
        css = {
            'all': ('/static/css/nhap.css', )
        }


admin_site = ASSSAdminSite(name='myapp')

admin_site.register(User)
admin_site.register(Role, RoleAdmin)
admin_site.register(House)
admin_site.register(Discount)
admin_site.register(Post)
admin_site.register(Comment)
admin_site.register(Booking)
admin_site.register(Follow)
admin_site.register(Image)

