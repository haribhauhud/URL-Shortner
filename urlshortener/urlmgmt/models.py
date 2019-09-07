from django.utils import timezone
from django.db import models
from django.conf import settings


class URL(models.Model):
    short_url = models.URLField(max_length=50, primary_key=True)
    http_url = models.URLField(unique=True)
    visitor_count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.http_url
