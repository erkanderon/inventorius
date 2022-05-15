from django.contrib import admin

from .models import Subnet, Ip


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subject", "created_on")


admin.site.register(Subnet)
admin.site.register(Ip)