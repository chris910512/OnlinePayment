from django.contrib import admin

from register.models import UserProfile, Admin

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Admin)
