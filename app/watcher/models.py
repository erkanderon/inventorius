from django.db import models
from common.models import NetworkConnDescription

# Create your models here.

STATUS = (
    (1,"Up"),
    (0,"Failed")
)

class Watcher(models.Model):
    dns = models.CharField(max_length=100)
    port = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS, default=0)
    error_code = models.ForeignKey(NetworkConnDescription, blank=True, null=True, related_name='error_code', on_delete=models.PROTECT)

    def __str__(self):
        return self.dns + ":" + self.port