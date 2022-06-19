from django.urls import path

from .views import settings, validate_regex_match

app_name = "settings"
urlpatterns = [
    path("settings", settings.as_view(), name="settings"),
    path("settings/check_regex", validate_regex_match, name="validate_regex_match"),
]