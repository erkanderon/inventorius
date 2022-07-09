from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
from django.http import JsonResponse

import re

from common.models import Description, Config
from .forms import RegexValidationForm, AddRegexForm, RemoveDescriptionForm, UpdateSMTPConfig

# Create your views here.
class settings(View):
    template_name = "pages/settings.html"
    success_url = "/settings"

    def get(self, request):

        desc = Description.objects.all()
        regex_form = RegexValidationForm()
        regex_add_form = AddRegexForm()
        regex_remove_form = RemoveDescriptionForm()
        smtp_update_form = UpdateSMTPConfig()
        config = Config.objects.get(id=1)
        

        return render(request, self.template_name, {'desc': desc, 
            'regex_form': regex_form, 
            'regex_add_form': regex_add_form, 
            'regex_remove_form': regex_remove_form,
            'smtp_update_form': smtp_update_form,
            'config': config})

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
                clean_form.delete()
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(self.success_url)

            messages.success(request, "Regex removed successfully!")
        return HttpResponseRedirect(self.success_url)

class update_smtp_config(View):
    success_url = "/settings"

    def post(self, request):
        form = UpdateSMTPConfig(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            try:
                config = Config.objects.get(id=1)
                config.smtp_uri = clean_form["smtp_uri"]
                config.smtp_port = clean_form["smtp_port"]
                config.save()
            except Exception as e:
                messages.error(request, e)
                return HttpResponseRedirect(self.success_url)

            messages.success(request, "SMTP updated successfully!")
        return HttpResponseRedirect(self.success_url)
