from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views import View
# Create your views here.


class watcher(View):
    template_name = "pages/watcher.html"
    success_url = "/watcher"

    def get(self, request):
        return render(request, self.template_name, {})