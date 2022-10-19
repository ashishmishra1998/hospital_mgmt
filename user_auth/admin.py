from django.contrib import admin
from user_auth.models import User_data
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

class UserModelAdmin(BaseUserAdmin):
    list_display = ('email', 'first_name','last_name','hospital','role','contact_no', 'is_admin')
    list_filter = ('is_admin','role',)
    fieldsets = (
        ('User Credentials', {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name','last_name','hospital','role','contact_no')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserModelAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name','last_name','hospital','role','contact_no','password1', 'password2'),
        }),
    )
    search_fields = ('email','hospital','role',)
    ordering = ('email','id')
    filter_horizontal = ()


# # Now register the new UserModelAdmin...
admin.site.register(User_data, UserModelAdmin)
