from django.urls import path

from .views import watcher, create, delete
app_name = "watcher"
urlpatterns = [
    path("watcher", watcher.as_view(), name="watcher"),
    path("watcher/delete", delete.as_view(), name="delete"),
    path("watcher/create", create.as_view(), name="create"),
]