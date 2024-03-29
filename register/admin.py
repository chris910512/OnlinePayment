from django.contrib import admin

from register.models import UserProfile, Currency, Admin

# Register your models here.

admin.site.register(Currency)
admin.site.register(UserProfile)
admin.site.register(Admin)
