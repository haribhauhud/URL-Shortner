from rest_framework import serializers
from .models import URL


class ShortURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ['short_url', 'http_url', 'visitor_count', 'created']