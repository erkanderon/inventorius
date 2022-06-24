from django.urls import path

from .views import watcher
app_name = "watcher"
urlpatterns = [
    path("watcher", watcher.as_view(), name="watcher"),
]