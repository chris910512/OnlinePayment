from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from register.models import UserProfile, Admin

admin.site.register(UserProfile)
admin.site.register(Admin)


class UserAdmin(BaseUserAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:
            Admin.objects.create(user=obj)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
