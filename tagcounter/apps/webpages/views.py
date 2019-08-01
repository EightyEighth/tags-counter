from rest_framework import response, status, viewsets
from rest_framework_extensions.cache.decorators import cache_response

from apps.contribe.utils import calculate_cache_key
from apps.webpages.tasks import fetch_url
from apps.webpages.models import WebPage
from apps.webpages.serializers import (WebPageSerializer,
                                       WebPageCreateSerializer)


class WebPageViewSet(viewsets.ViewSet):

    def create(self, request, *args, **kwargs):
        serializer = WebPageCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        fetch_url.delay(serializer.data.get('url'))

        return response.Response({'status': 'ok'},
                                 status=status.HTTP_201_CREATED)

    @cache_response(60*60*2, key_func=calculate_cache_key)
    def retrieve(self, request, *args, **kwargs):
        url = request.query_params.get('url', None)
        web_page = WebPage.objects.get(url=url)
        if not web_page:
            return response.Response({'status': 'not found'},
                                     status=status.HTTP_404_NOT_FOUND)
        return response.Response(
            data=WebPageSerializer(web_page).data,
            status=status.HTTP_200_OK)
