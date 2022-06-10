
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.views import View

from .forms import EnvironmentForm, RemoveEnvironmentForm
from .models import Environment

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
                form.save()
                messages.success(request, "Environment created successfully!")
                return HttpResponseRedirect(request.path)
            messages.warning(request, "Environment already exist!")
            return HttpResponseRedirect(request.path)
        messages.error(request, "Environment created failed!")
        return HttpResponseRedirect(request.path)

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