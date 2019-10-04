from django.db import models


class TimeStampedModel(models.Model):
    """a model with timestamps"""
    created = models.DateTimeField(auto_now_add=True)

    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
