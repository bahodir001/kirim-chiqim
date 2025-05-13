from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, FamilyGroup
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    model = CustomUser
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'card_number', 'family_group', 'role_in_family', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'family_group', 'role_in_family')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('email',)
    readonly_fields = ('profile_preview',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Shaxsiy ma’lumotlar', {'fields': ('first_name', 'last_name', 'phone_number', 'card_number', 'profile_photo', 'profile_preview')}),
        ('Guruh', {'fields': ('family_group', 'role_in_family')}),
        ('Ruxsatlar', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Muhim sana', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'first_name', 'last_name', 'card_number', 'password1', 'password2')}
        ),
    )

    def profile_preview(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" width="50" height="50" style="border-radius:50%;" />', obj.profile_photo.url)
        return "(Rasm yo'q)"
    profile_preview.short_description = "Profil rasmi"

# Guruh modeli uchun admin
@admin.register(FamilyGroup)
class FamilyGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
