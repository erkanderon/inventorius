from django.urls import path

from .views import get_homepage

app_name = "homepage"
urlpatterns = [
    path("", get_homepage, name="homepage"),
]