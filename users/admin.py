from django.contrib import admin
from .models import Custom_User
# admin.site.register(User)
@admin.register(Custom_User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'phone', 'is_active', 'is_superuser']
