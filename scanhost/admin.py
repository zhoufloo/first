from django.contrib import admin

from .models import Server, User

class ServerAdmin(admin.ModelAdmin):

    list_display = ['IP', 'server_type', 'created_by']

    list_filter = ['server_type', 'created_by']

    search_fields = ['IP']



class UserAdmin(admin.ModelAdmin):

    list_display = ['username', 'password', 'pkey', 'server']





# Register your models here.

admin.site.register(Server, ServerAdmin)

admin.site.register(User, UserAdmin)