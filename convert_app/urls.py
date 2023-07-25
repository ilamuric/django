# convert_app/urls.py

from django.urls import path
from . import views

app_name = "convert_app"

urlpatterns = [
    path('', views.convert_image, name='convert_image'),
]
