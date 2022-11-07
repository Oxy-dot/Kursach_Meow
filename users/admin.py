from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    # add_form = CustomUserCreationForm
    # form = CustomUserChangeForm

    list_display = ['username', 'fullName', 'email', 'phoneNumber', 'adress', 'is_staff']
    list_display_links =['email']
    # Add user
    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Custom fields',
            {
                'fields': (
                    'fullName',
                    'email',
                    'phoneNumber',
                    'adress',
                )
            }
        )
    )
    fieldsets = (
        (None, {
            'fields': ('fullName', 'username','email','adress','phoneNumber','is_staff'),
        }),
    )
    # Edit user
    list_editable = ['fullName', 'phoneNumber', 'adress']



