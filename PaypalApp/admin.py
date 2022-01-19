from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,transactionsModel
from .forms import CustomUserCreationForm


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm

    fieldsets = (
        *UserAdmin.fieldsets,
        (
            'Reference Id',
            {
                'fields': (
                    'Refrence_Id',
                )
            }
        )
    )


admin.site.register(CustomUser)
admin.site.register(transactionsModel)