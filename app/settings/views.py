from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse

import re

from common.models import Description
from .forms import RegexValidationForm, AddRegexForm, RemoveDescriptionForm

# Create your views here.
class settings(View):
    template_name = "pages/settings.html"
    success_url = "/settings"

    def get(self, request):

        desc = Description.objects.all()
        regex_form = RegexValidationForm()
        regex_add_form = AddRegexForm()
        regex_remove_form = RemoveDescriptionForm()
        

        return render(request, self.template_name, {'desc': desc, 'regex_form': regex_form, 'regex_add_form': regex_add_form, 'regex_remove_form': regex_remove_form})

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

class add_description(View):
    success_url = "/settings"

    def post(self, request):
        form = AddRegexForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            description = Description.objects.create(regex_name=clean_form["regex_name"], regex=clean_form["regex"], description=clean_form["description"])
            description.save()

            messages.success(request, "Regex added successfully!")
        return HttpResponseRedirect(self.success_url)

class delete_description(View):
    success_url = "/settings"

    def post(self, request):
        form = RemoveDescriptionForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            try:
                description = Description.objects.get(description=clean_form["regex_name"])
                description.delete()
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(self.success_url)

            messages.success(request, "Regex removed successfully!")
        return HttpResponseRedirect(self.success_url)
