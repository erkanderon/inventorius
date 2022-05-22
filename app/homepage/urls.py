from django.urls import path

from .views import home_page

app_name = "homepage"
urlpatterns = [
    path("", home_page, name="homepage"),
]