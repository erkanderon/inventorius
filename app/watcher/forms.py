from django import forms

from .models import Watcher


class CreateWatcherForm(forms.ModelForm):
    dns = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    port = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    #environment = forms.ModelChoiceField(required=True, queryset=Environment.objects.all(), widget=forms.Select(attrs={'class': 'form-select me-sm-2 wide'}), empty_label="Nothing Selected")
    
    class Meta:
        model = Watcher
        fields = ["dns", "port"]

class RemoveWatcherForm(forms.ModelForm):
    dns = forms.ModelChoiceField(required=True, queryset=Watcher.objects.all(), widget=forms.Select(attrs={'class': 'form-select me-sm-2 wide'}), empty_label="Nothing Selected")

    class Meta:
        model = Watcher
        fields = ["dns"]