

from django import forms
import re
from common.models import Description

class RegexValidationForm(forms.Form):
    regex = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder': '^dpdb.*p.*$'}))
    word = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder': '...'}))

    
class AddRegexForm(forms.ModelForm):
    regex_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    regex = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control', 'style': 'height: 144px;'}))
    
    class Meta:
        model = Description
        fields = ["regex_name", "regex", "description"]

class RemoveDescriptionForm(forms.ModelForm):
    regex_name = forms.ModelChoiceField(required=True, queryset=Description.objects.all(), widget=forms.Select(attrs={'class': 'form-select me-sm-2 wide'}), empty_label="Nothing Selected")

    class Meta:
        model = Description
        fields = ["regex_name"]