from django.contrib import admin
from .models import Post,House,Comment,PostingPrice,Discount,Role,Image,Follow,Booking,User
# Register your models here.


class RoleAdmin(admin.ModelAdmin):
    list_display = ['id', 'rolename']
    search_fields = ['rolename']
    list_filter = ['id', 'rolename']


admin.site.register(User)
admin.site.register(Role, RoleAdmin)
admin.site.register(House)
admin.site.register(Discount)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostingPrice)
admin.site.register(Booking)
admin.site.register(Follow)
admin.site.register(Image)

