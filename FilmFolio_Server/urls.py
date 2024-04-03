from django.contrib import admin
from django.urls import path
from api.views import app

urlpatterns = [path("admin/", admin.site.urls), path("", app.urls)]
