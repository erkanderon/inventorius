from django.urls import path

from .views import ContactFormView

app_name = "homepage"
urlpatterns = [
    path("", ContactFormView.as_view(), name="homepage"),
]