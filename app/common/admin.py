from django.contrib import admin
from .models import Description, NetworkConnDescription, Config
# Register your models here.

admin.site.register(Description)
admin.site.register(NetworkConnDescription)
admin.site.register(Config)