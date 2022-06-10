
from django import forms

from .models import Environment
from common.models import Description


class EnvironmentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    regex = forms.ModelChoiceField(required=True, queryset=Description.objects.all(), widget=forms.Select(attrs={'class': 'form-select me-sm-2 wide'}), empty_label="Nothing Selected")
    
    class Meta:
        model = Environment
        fields = ["name", "regex"]


class RemoveEnvironmentForm(forms.ModelForm):
    name = forms.ModelChoiceField(required=True, queryset=Environment.objects.all(), widget=forms.Select(attrs={'class': 'form-select me-sm-2 wide'}), empty_label="Nothing Selected")

    class Meta:
        model = Environment
        fields = ["name"]

    