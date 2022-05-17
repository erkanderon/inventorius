
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages

from .forms import SubnetForm
from .models import NMAPTask, Subnet
from .runners import start_nmap_analyze


def get_homepage(request):
    template_name = "pages/homepage.html"
    success_url = "/"

    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubnetForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            clean_form = form.cleaned_data
        
            running_task = NMAPTask.objects.filter(flag="1").exists()
            if running_task:
                messages.error(request, "There is Already a Running Task.")
                return HttpResponseRedirect(request.path)

            subnet = Subnet.objects.filter(subnet_ip=clean_form["subnet_ip"]).exists()
            if not subnet:
                form.save()
        
            start_nmap_analyze(clean_form)
            messages.success(request, "Job started successfully!")
            return HttpResponseRedirect(request.path)
    else:
        form = SubnetForm()
    return render(request, template_name, {'form': form})
