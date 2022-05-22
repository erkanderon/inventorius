
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages


def home_page(request):
    template_name = "pages/homepage.html"

    return render(request, template_name, {'form': {}})
