from django.db import models


class MainModelManager(models.Manager):
    def get(self, *args, **kwargs):
        try:
            return super(MainModelManager, self).get(*args, **kwargs)
        except self.model.DoesNotExist:
            return None


class MainModel(models.Model):
    objects = MainModelManager()

    class Meta:
        abstract = True
