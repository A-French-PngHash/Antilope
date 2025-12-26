from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Activity

admin.site.register(User)
admin.site.register(Activity)