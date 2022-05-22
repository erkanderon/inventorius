from django.forms import ModelForm

from .models import Subnet


class SubnetForm(ModelForm):
    class Meta:
        model = Subnet
        fields = ["subnet_ip", "mask"]