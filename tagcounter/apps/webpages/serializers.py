from django.core.validators import URLValidator
from rest_framework import serializers, exceptions

from apps.webpages.models import WebPage


class WebPageCreateSerializer(serializers.Serializer):
    url = serializers.URLField(required=True)

    class Meta:
        fields = '__all__'

    def validate_url(self, val):
        validator = URLValidator(schemes=['http', 'https'])
        try:
            validator(val)
        except exceptions.ValidationError:
            raise exceptions.ValidationError('URL is not correct format.')

        return val


class WebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebPage
        fields = '__all__'
