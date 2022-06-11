
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View
import re

from .forms import EnvironmentForm, RemoveEnvironmentForm
from .models import Environment
from common.models import Description
from subnet.models import Ip
from common.runner import sync_ip_description

class environment(View):
    template_name = "pages/environment.html"
    success_url = "/environment"

    def get(self, request):
        remove_form = RemoveEnvironmentForm()
        form = EnvironmentForm()
        environment = Environment.objects.all()

        return render(request, self.template_name, {"form": form, "environment": environment, "remove_form": remove_form})

    def post(self, request):
        form = EnvironmentForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            clean_form = form.cleaned_data

            environment = Environment.objects.filter(name=clean_form["name"]).exists()
            if not environment:
                sync_ip_description()
                ip_count = Ip.objects.filter(description=clean_form["regex"]).values("ip").distinct().count()
                form.save()
                environment = Environment.objects.get(name=clean_form["name"])
                environment.count = ip_count
                environment.save()
                messages.success(request, "Environment created successfully!")
                return HttpResponseRedirect(request.path)
            messages.warning(request, "Environment already exist!")
            return HttpResponseRedirect(request.path)
        messages.error(request, "Environment created failed!")
        return HttpResponseRedirect(request.path)

    def _sync_ip_description(self):
        descriptions = Description.objects.all()
        ip = Ip.objects.all()
        for ip_obj in ip.iterator():
            for desc in descriptions.iterator():
                if re.search(desc.regex, ip_obj.dns):
                    ip_obj.description.add(desc)
            ip_obj.save()

class delete_environment(View):
    template_name = "pages/environment.html"
    success_url = "/environment"

    def post(self, request):
        form = RemoveEnvironmentForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            environment = Environment.objects.get(name=clean_form["name"])
            environment.delete()

            messages.success(request, "Environment removed successfully!")
        return HttpResponseRedirect(self.success_url)