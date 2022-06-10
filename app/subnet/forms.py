from django import forms

from .models import Subnet


class SubnetForm(forms.ModelForm):
    subnet_ip= forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    mask= forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))

    class Meta:
        model = Subnet
        fields = ["subnet_ip", "mask"]