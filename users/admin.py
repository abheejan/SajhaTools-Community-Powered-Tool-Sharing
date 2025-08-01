from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser

    list_display = ['username', 'email', 'first_name', 'last_name', 'is_staff', 'tool_count']

    def tool_count(self, obj):
        count = obj.tool_set.count()
        # The 'obj.pk' is the user's primary key (ID)
        url = reverse('admin:tools_tool_changelist') + f'?owner__id__exact={obj.pk}'
        return format_html('<a href="{}">{} Tools</a>', url, count)
        
    tool_count.short_description = 'Tools Owned' # Sets the column header text

admin.site.register(CustomUser, CustomUserAdmin)
