from django.contrib import admin

from .models import Subnet, Ip, NMAPTask, Description


class ContactFormAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "subject", "created_on")


admin.site.register(Subnet)
admin.site.register(Ip)
admin.site.register(NMAPTask)
admin.site.register(Description)