from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
# Create your views here.

from .forms import CreateWatcherForm, RemoveWatcherForm
from .models import Watcher
from common.runner import check_machine_connection
from common.models import NetworkConnDescription


class watcher(View):
    template_name = "pages/watcher.html"
    success_url = "/watcher"

    def get(self, request):
        create_form = CreateWatcherForm()
        remove_form = RemoveWatcherForm()
        watcher = Watcher.objects.all()

        return render(request, self.template_name, { 
        	"create_form": create_form, 
        	"remove_form": remove_form,
        	"watcher": watcher})

class create(View):
    template_name = "pages/watcher.html"
    success_url = "/watcher"

    def post(self, request):
        form = CreateWatcherForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            clean_form = form.cleaned_data
            dns = clean_form["dns"]
            port = port=clean_form["port"]

            is_watcher_exist = Watcher.objects.filter(dns=dns, port=port).exists()
            if not is_watcher_exist:
                response_code, status = check_machine_connection(dns, port)
                print(response_code, status)
                watcher = Watcher()
                watcher.dns = dns
                watcher.port = port
                watcher.status = status
                try:
                    watcher.error_code = NetworkConnDescription.objects.get(code=response_code)
                except Exception as e:
                    watcher.error_code = NetworkConnDescription.objects.get(code=1001)
                watcher.save()
                messages.success(request, "Watcher created successfully!")
                return HttpResponseRedirect(self.success_url)
            messages.warning(request, "Watcher already exist!")
            return HttpResponseRedirect(self.success_url)
        messages.error(request, "Watcher creation failed!")
        return HttpResponseRedirect(self.success_url)

class delete(View):
    success_url = "/watcher"

    def post(self, request):
        form = RemoveWatcherForm(request.POST)

        if form.is_valid():
            clean_form = form.cleaned_data
            host_port = clean_form["dns"]

            host_port.delete()

            messages.success(request, "Watcher removed successfully!")
        return HttpResponseRedirect(self.success_url)