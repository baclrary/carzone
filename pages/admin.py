from django.contrib import admin
from django.utils.html import format_html
from .models import Team, Office, OfficeHours

class TeamAdmin(admin.ModelAdmin):
    def thumbnail(self, team_member: Team):
        return format_html(f'<img src="{team_member.photo.url}" width="40" style="border-radius: 50px" />')
    
    thumbnail.short_description = "Photo"
    
    list_display = ('id', 'thumbnail', 'first_name', 'last_name', 'designation', 'created_date')
    list_display_links = ('id', 'thumbnail', 'first_name')
    search_fields = ('first_name', 'last_name', 'designation')
    list_filter = ('designation', )

admin.site.register(Team, TeamAdmin)

class OfficeHoursInline(admin.TabularInline):
    model = OfficeHours
    extra = 1

class OfficeAdmin(admin.ModelAdmin):
    def staff_count(self, obj: Office) -> int:
        """Returns the count of team members associated with the office."""
        return obj.office_staff.count()
    
    inlines = [OfficeHoursInline]
    list_display = ('name', 'city', 'state', 'country', 'phone', 'email', 'staff_count', 'created_at', 'updated_at')
    list_filter = ('city', 'state', 'country')
    search_fields = ('name', 'city', 'state', 'country')
    date_hierarchy = 'created_at'

admin.site.register(Office, OfficeAdmin)
