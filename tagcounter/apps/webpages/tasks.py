import requests

from tagcounter.celery import app
from apps.webpages.models import WebPage
from apps.webpages.parsers import CountTagsHtmlParser


@app.task
def fetch_url(url):
    response = requests.get(url)

    parser = CountTagsHtmlParser()
    parser.feed(response.text)
    web_page = WebPage.objects.get(tags=dict(parser.tags()), url=url)
    if not web_page:
        WebPage.objects.update_or_create(
            url=url, defaults={'tags': dict(parser.tags())})
