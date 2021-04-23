from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdmin(DefaultUserAdmin):
    list_filter = []
    list_display = ['username']
    filter_horizontal = []
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
