from django.urls import path

from .views import subnet_page

app_name = "subnet"
urlpatterns = [
    path("subnet", subnet_page, name="subnet"),
]