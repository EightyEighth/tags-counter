from django.contrib.postgres.fields import JSONField
from django.db import models

from apps.contribe.models import MainModel


class WebPage(MainModel):
    tags = JSONField()
    timestamp = models.DateTimeField(auto_now_add=True)
    url = models.URLField(unique=True)

    class Meta:
        db_table = 'webpages'

    def __str__(self):
        return f'{self.__class__.__name__}: {self.pk}'
