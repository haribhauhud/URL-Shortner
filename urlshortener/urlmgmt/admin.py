from django.contrib import admin
from .models import URL

# Register your models here.


class UrlsAdmin(admin.ModelAdmin):
    list_display = ('short_url', 'http_url', 'created', 'visitor_count')
    ordering = ('-created',)


admin.site.register(URL, UrlsAdmin)  # Register the Urls model with UrlsAdmin options
