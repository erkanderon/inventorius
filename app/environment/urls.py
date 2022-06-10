from django.urls import path

from .views import environment, delete_environment

app_name = "environment"
urlpatterns = [
    path("environment", environment.as_view(), name="environment"),
    path("environment/delete", delete_environment.as_view(), name="delete_environment"),
]