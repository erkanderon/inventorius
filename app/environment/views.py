
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View

from .forms import EnvironmentForm, RemoveEnvironmentForm, UpdateEnvironmentForm
from .models import Environment
from common.models import Description
from subnet.models import Ip
from common.runner import sync_ip_description, sync_environment_count

class environment(View):
    template_name = "pages/environment.html"
    success_url = "/environment"

    def get(self, request):
        remove_form = RemoveEnvironmentForm()
        form = EnvironmentForm()
        update_form = UpdateEnvironmentForm()
        environment = Environment.objects.all()

        return render(request, self.template_name, {"form": form, "environment": environment, "remove_form": remove_form, "update_form": update_form})

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

class delete(View):
    success_url = "/environment"

    def post(self, request):
        form = RemoveEnvironmentForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            environment = Environment.objects.get(name=clean_form["name"])
            environment.delete()

            messages.success(request, "Environment removed successfully!")
        return HttpResponseRedirect(self.success_url)

class update(View):
    success_url = "/environment"

    def post(self, request):
        form = UpdateEnvironmentForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data

            environment = Environment.objects.get(id=clean_form["id"])
            environment.name = clean_form["name"]
            environment.regex = Description.objects.get(description=clean_form["regex"])
            environment.save()

            sync_environment_count()

            messages.success(request, "Environment updated successfully!")
        else:
            print("form clean değil")
        return HttpResponseRedirect(self.success_url)

class detail(View):
    template_name = "pages/environment/detail.html"
    success_url = "/environment"

    def get(self, request, *args, **kwargs):

        id = self.kwargs["id"]

        environment = Environment.objects.get(id=id)
        ips = Ip.objects.filter(description=environment.regex)
        ip_count = Ip.objects.filter(description=environment.regex)
        dns_count = Ip.objects.filter(description=environment.regex)

        return render(request, self.template_name, {'ips': ips, 'ip_count': ip_count, 'dns_count': dns_count, 'environment': environment})