from django.contrib import admin
from .models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "phone", "car_title", "state", "city", "created_at")
    list_display_links = ("id", "first_name", "last_name", "email", "phone")
    search_fields = ("email", "phone", "car_title")
    list_per_page = 25


admin.site.register(Contact, ContactAdmin)
