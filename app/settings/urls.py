from django.urls import path

from .views import settings, validate_regex_match, add_description, delete_description

app_name = "settings"
urlpatterns = [
    path("settings", settings.as_view(), name="settings"),
    path("settings/check_regex", validate_regex_match, name="validate_regex_match"),
    path("settings/description/delete", delete_description.as_view(), name="delete_description"),
    path("settings/description/add", add_description.as_view(), name="delete_description"),
]