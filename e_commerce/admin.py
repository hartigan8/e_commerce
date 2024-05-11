from django.contrib import admin

from . import models
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Customer

# Inline class for Customer details within User admin
class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = "customers"

# New User admin that includes Customer details
class UserAdmin(BaseUserAdmin):
    inlines = [CustomerInline]

# Unregister the original User admin if it is registered
if admin.site.is_registered(User):
    admin.site.unregister(User)

# Register the new User admin that includes Customer details


admin.site.register(models.Product)
admin.site.register(models.Comment)
admin.site.register(User, UserAdmin)
