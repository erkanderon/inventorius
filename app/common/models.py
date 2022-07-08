from django.db import models

# Create your models here.
class Description(models.Model):
    regex_name = models.CharField(max_length=100)
    regex = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description

class NetworkConnDescription(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.description