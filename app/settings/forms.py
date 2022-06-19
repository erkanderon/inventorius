

from django import forms
import re
from common.models import Description

class RegexValidationForm(forms.Form):
    regex = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder': '^dpdb.*p.*$'}))
    word = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control form-control-sm', 'placeholder': '...'}))

    
