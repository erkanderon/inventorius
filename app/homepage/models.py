from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Subnet(models.Model):
    subnet_ip = models.GenericIPAddressField()
    mask = models.IntegerField(
        default=30,
        validators=[MaxValueValidator(30), MinValueValidator(8)]
    )
    cidr = models.CharField(max_length=20, default="None", editable=False)

    def save(self, *args, **kwargs):
        concat = str(self.subnet_ip) + "/" + str(self.mask)
        self.cidr = concat
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cidr

class Ip(models.Model):

    ip = models.CharField(max_length=100)
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
    dns = models.CharField(max_length=100, null=True)
    description = models.CharField(max_length=1000)

class NMAPTask(models.Model):
    CHOICES = (
        ("0", 'Finished'),
        ("1", 'Running'),
        ("2", 'Failed'),
        ("3", 'Not Started')
    )

    task_id = models.CharField(max_length=100)
    took_time_in_minute = models.IntegerField(default=0)
    flag = models.CharField(max_length=1, choices=CHOICES, default="3")

    def __str__(self):
        return str(self.id) + " - " + self.task_id
