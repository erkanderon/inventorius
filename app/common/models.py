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
    code = models.IntegerField(default=None)
    description = models.TextField(blank=True)

    def __str__(self):
        return str(self.code)

class Config(models.Model):
    smtp_uri = models.CharField(max_length=100, default=None)
    smtp_port = models.IntegerField(default=None)
    smtp_sender = models.CharField(max_length=100, default=None, null=True)
    smtp_receiver = models.CharField(max_length=200, default=None, null=True)
    smtp_subject = models.CharField(max_length=100, default=None, null=True)
    smtp_enabled = models.BooleanField(default=False)

    def __str__(self):
        return "configuration"