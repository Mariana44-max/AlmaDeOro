from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile, Address


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'


class AddressInline(admin.TabularInline):
    model = Address
    extra = 0
    verbose_name_plural = 'Addresses'


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [ProfileInline, AddressInline]
    list_display = ['email', 'username', 'full_name', 'is_admin', 'is_staff', 'date_joined']
    list_filter = ['is_admin', 'is_staff', 'is_active', 'date_joined']
    search_fields = ['email', 'username', 'full_name']
    ordering = ['-date_joined']

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Custom Fields', {
            'fields': ('full_name', 'is_admin')
        }),
    )


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'date_of_birth', 'created_at']
    search_fields = ['user__email', 'user__username', 'phone']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['label', 'user', 'full_name', 'city', 'state', 'country', 'is_default', 'address_type']
    list_filter = ['is_default', 'address_type', 'country', 'state']
    search_fields = ['user__email', 'label', 'full_name', 'city', 'address_line_1']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-is_default', '-created_at']

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'label', 'address_type', 'is_default')
        }),
        ('Contact Details', {
            'fields': ('full_name', 'phone')
        }),
        ('Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'state', 'zip_code', 'country')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
