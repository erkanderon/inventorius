from django.urls import path

from .views import environment, delete, update, detail

app_name = "environment"
urlpatterns = [
    path("environment", environment.as_view(), name="environment"),
    path("environment/delete", delete.as_view(), name="delete"),
    path("environment/update", update.as_view(), name="update"),
    path("environment/<str:id>/detail", detail.as_view(), name="detail"),
    
]