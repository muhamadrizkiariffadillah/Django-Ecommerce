from django.contrib import admin
from .models import User, UsersProfile

# Register your models here.

admin.site.register(User)
admin.site.register(UsersProfile)