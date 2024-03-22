from django.contrib import admin
from provider.models import *

class Provider_Admin(admin.ModelAdmin):
    list_display = ('Provider_Name', 'Provider_ID')
    list_display_links = ['Provider_ID']
    ordering = ['Provider_Name']
    search_fields = ['Provider_ID__iexact', 'Provider_Name']

# Register your models here.
admin.site.register(Provider, Provider_Admin)
