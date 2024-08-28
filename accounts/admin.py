from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserAccount, PublisherProfile, AdvertiserProfile

class CustomUserAdmin(UserAdmin):
    model = UserAccount
    list_display = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active',)
    list_filter = ('email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('user_type', 'is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'user_type', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email', 'first_name', 'last_name',)
    ordering = ('email',)

admin.site.register(UserAccount, CustomUserAdmin)

@admin.register(PublisherProfile)
class PublisherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')

@admin.register(AdvertiserProfile)
class AdvertiserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
    search_fields = ('user__email', 'user__first_name', 'user__last_name', 'phone')