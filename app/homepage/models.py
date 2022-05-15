from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


class Subnet(models.Model):
    subnet_ip = models.GenericIPAddressField()
    mask = models.IntegerField(
        default=0,
        validators=[MaxValueValidator(32), MinValueValidator(0)]
    )
    cidr = models.CharField(max_length=20, default="None", editable=False)

    def save(self, *args, **kwargs):
        concat = str(self.subnet_ip) + "/" + str(self.mask)
        self.cidr = concat
        super().save(*args, **kwargs)

    def __str__(self):
        return self.cidr

class Ip(models.Model):
    CHOICES = (
        ("0", 'Reserved'),
        ("1", 'Non Reserved'),
        ("2", 'New One')
    )

    ip = models.CharField(max_length=100)
    subnet = models.ForeignKey(Subnet, on_delete=models.CASCADE)
    dns = models.CharField(max_length=100, null=True)
    flag = models.CharField(max_length=1, choices=CHOICES, default="2")
    description = models.CharField(max_length=1000)
