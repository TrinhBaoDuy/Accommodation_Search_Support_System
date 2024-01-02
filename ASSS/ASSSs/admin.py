from django.contrib import admin
from django.shortcuts import render
from django.template.response import TemplateResponse

from . import dao
from .models import Post,House,Comment,PostingPrice,Discount,Role,Image,Follow,Booking,User
from django.urls import path
# Register your models here.


class ASSSAdminSite(admin.AdminSite):
    site_header = 'Quan Ly He Thong'

    def get_urls(self):
        return [
                   path('ASSS-stats/', self.stats_view)
               ] + super().get_urls()

    def stats_view(self, request):
        return TemplateResponse(request, 'admin/nhap.html', {
            'stats': dao.count_image_by_house(),
            'houses': dao.load_houses(),
            'statsUser': dao.count_user_by_role(),
            'users': dao.load_user(),
            'stats_user_role_by_year': dao.count_user_role_by_year(),
            'stats_user_role_by_month': dao.count_users_each_month_of_the_year(),
            'stats_user_role_by_quarter': dao.count_users_each_quarter_of_the_year(),
            'count_host': dao.count_host(),
            'count_user': dao.count_host(),

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
admin_site.register(PostingPrice)
admin_site.register(Booking)
admin_site.register(Follow)
admin_site.register(Image)

