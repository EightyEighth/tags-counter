import json
import mock

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import test, status

from apps.webpages.models import WebPage
from apps.webpages.parsers import CountTagsHtmlParser
from apps.webpages.tasks import fetch_url
from apps.webpages.views import WebPageViewSet


class PrepareTests(test.APITestCase):
    def setUp(self):
        self.html = '<html><head><title>Test</title></head>' \
                    '<body><br><h1>Parse me!</h1><br><img src="tes.png">' \
                    '</body></html>'
        self.url = 'https://fackeurl.com/index.html'
        self.factory = test.APIRequestFactory()
        cache.clear()


class ModelsTests(TestCase):
    def test_webpage_model_fields(self):
        web_page = WebPage()

        self.assertTrue(hasattr(web_page, 'tags'))
        self.assertTrue(hasattr(web_page, 'timestamp'))
        self.assertTrue(hasattr(web_page, 'url'))

    def test_webpage_model_plural(self):
        self.assertEqual(WebPage._meta.verbose_name_plural, 'web pages')

    def test_webpage_model_table_name(self):
        self.assertEqual(WebPage._meta.db_table, 'webpages')

    def test_webpage_model_string_representation(self):
        web_page = WebPage()

        self.assertEqual(str(web_page), 'WebPage: {}'.format(web_page.pk))


class ParsersTests(PrepareTests):
    def test_html_parser(self):
        parser = CountTagsHtmlParser()
        parser.feed(self.html)

        result = parser.tags()

        self.assertEqual(result['html'], 1)
        self.assertEqual(result['head'], 1)
        self.assertEqual(result['title'], 1)
        self.assertEqual(result['body'], 1)
        self.assertEqual(result['h1'], 1)
        self.assertEqual(result['br'], 2)
        self.assertEqual(result['img'], 1)

    def test_html_parser_with_json_response(self):
        _json = json.dumps({'error': 'test error', 'code': 400})

        parser = CountTagsHtmlParser()
        parser.feed(json.dumps(_json))

        result = parser.tags()

        self.assertEqual(len(result), 0)


class ViewsTests(PrepareTests):

    def test_retrieve_method_webpage(self):
        web = WebPage.objects.create(
            tags={'html': 1, 'body': 1},
            url=self.url)

        url = reverse('api:webpages-list')

        request = self.factory.get(url, {'url': self.url})

        view = WebPageViewSet.as_view({'get': 'retrieve'})

        response = view(request).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['tags']['html'],
                         web.tags['html'])
        self.assertEqual(json.loads(response.content)['url'],
                         web.url)

    def test_retrieve_method_webpage_twice_with_dif_urls(self):
        web1 = WebPage.objects.create(
            tags={'html': 1, 'body': 1},
            url=self.url)

        custom_url = 'http://example.com/index.html'
        web2 = WebPage.objects.create(
            tags={'html': 1, 'body': 1, 'a': 1},
            url=custom_url)

        url = reverse('api:webpages-list')

        request = self.factory.get(url, {'url': self.url})

        view = WebPageViewSet.as_view({'get': 'retrieve'})

        response = view(request).render()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['tags']['html'],
                         web1.tags['html'])
        self.assertEqual(json.loads(response.content)['url'],
                         web1.url)

        url = reverse('api:webpages-list')

        request = self.factory.get(url, {'url': custom_url})

        view = WebPageViewSet.as_view({'get': 'retrieve'})

        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['tags']['a'],
                         web2.tags['a'])

    @mock.patch('apps.webpages.tasks.requests.get')
    @mock.patch('apps.webpages.tasks.fetch_url.delay', side_effect=fetch_url)
    def test_create_method_webpage(self, mock_get, mock_delay):
        mock_delay.return_value.get.return_value = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.html

        url = reverse('api:webpages-list')

        request = self.factory.post(
            url, data={'url': self.url})

        view = WebPageViewSet.as_view({'post': 'create'})

        response = view(request).render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WebPage.objects.get().url, self.url)

    @mock.patch('apps.webpages.tasks.requests.get')
    @mock.patch('apps.webpages.tasks.fetch_url.delay', side_effect=fetch_url)
    def test_create_method_webpage_twice_the_same_url(self, mock_get,
                                                      mock_delay):
        mock_delay.return_value.get.return_value = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.html

        url = reverse('api:webpages-list')

        request = self.factory.post(
            url, data={'url': self.url})

        view = WebPageViewSet.as_view({'post': 'create'})

        response = view(request).render()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WebPage.objects.get().url, self.url)


class TasksTest(PrepareTests):
    @mock.patch('requests.get')
    def test_fetch_url(self, mock_resp):
        mock_resp.return_value.status_code = 200
        mock_resp.return_value.text = self.html

        fetch_url(self.url)

        self.assertEqual(WebPage.objects.count(), 1)
        self.assertEqual(WebPage.objects.get().url, self.url)
        self.assertEqual(WebPage.objects.get().tags['html'], 1)


class APITests(PrepareTests):

    def test_get_method(self):
        web_page = WebPage.objects.create(
            url=self.url,
            tags={'html': 1, 'body': 1})

        url = reverse('api:webpages-list')
        response = self.client.get(url, {'url': self.url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['tags']['html'],
                         web_page.tags['html'])
        self.assertEqual(json.loads(response.content)['url'],
                         web_page.url)
        self.assertEqual(web_page.url, self.url)

    def test_get_method_data_not_found(self):
        url = reverse('api:webpages-list')
        response = self.client.get(url, {'url': self.url})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_method_from_cache(self, ):
        WebPage.objects.create(url=self.url, tags={'html': 1, 'body': 1})

        url = reverse('api:webpages-list')
        response = self.client.get(url, {'url': self.url})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        with mock.patch('django.core.cache.cache.get') as mock_cache_get:
            mock_cache_get.return_value = (response.content,
                                           response.status_code,
                                           response._headers)

            response = self.client.get(url, {'url': self.url})

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(mock_cache_get.call_count, 1)

    @mock.patch('apps.webpages.tasks.requests.get')
    @mock.patch('apps.webpages.tasks.fetch_url.delay', side_effect=fetch_url)
    def test_post_method(self, mock_get, mock_delay):
        mock_delay.return_value.get.return_value = None
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = self.html

        web_page = WebPage.objects.create(
            url=self.url,
            tags={'html': 1, 'body': 1})

        url = reverse('api:webpages-list')
        response = self.client.post(
            url, data={'url': self.url, 'tags': {'html': 1, 'body': 1}},
            format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(web_page.url, self.url)
