from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse

import re

from common.models import Description
from .forms import RegexValidationForm

# Create your views here.
class settings(View):
    template_name = "pages/settings.html"
    success_url = "/settings"

    def get(self, request):

        desc = Description.objects.all()
        regex_form = RegexValidationForm()

        return render(request, self.template_name, {'desc': desc, 'regex_form': regex_form})

    def post(self, request):
        form = RegexValidationForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            clean_form = form.cleaned_data
            return HttpResponseRedirect("/")
        print(form.errors)
        return HttpResponseRedirect(request.path)

def validate_regex_match(request):
    regex = request.GET.get('regex', None)
    word = request.GET.get('word', None)

    data = {
        'result': ""
    }

    res = re.search(regex, word)
    if res:
        data["result"] = "true"
    else:
        data["result"] = "false"
    
    return JsonResponse(data)
