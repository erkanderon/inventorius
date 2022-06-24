from django.db import models

from common.models import Description


class Environment(models.Model):
    name = models.CharField(max_length=100)
    regex = models.ForeignKey(Description, related_name='regex_description', blank=True, null=True, on_delete=models.PROTECT)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.name
