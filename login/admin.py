# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from models import Pro
from django.contrib.auth.models import User


# Register your models here.


class ProInline(admin.StackedInline):
    model = Pro


class CustomUserAdmin(UserAdmin):
    inlines = [
        ProInline,
    ]
    list_display = ('username', 'first_name', 'phone')
    ordering = ('username',)
    list_filter = ('username', 'first_name', 'pro__id_num', 'pro__phone')

    def phone(self, obj):
        return obj.pro.phone
    phone.short_description = "电话"


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
