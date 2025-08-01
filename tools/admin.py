from django.contrib import admin
from .models import Tool

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):

    # Fields to display in the main list view
    list_display = ('name', 'owner', 'availability_status', 'average_rating', 'posted_time')
    
    # Filters that appear on the right-hand side
    list_filter = ('availability_status', 'posted_time')
    
    # Fields to search by. We can even search by the owner's username.
    search_fields = ('name', 'description', 'owner__username')
    
    # Enables the default "delete selected" action in the dropdown.
    actions = ['delete_selected']