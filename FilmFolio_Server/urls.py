from django.contrib import admin
from django.urls import path
from api.views import app
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [path("admin/", admin.site.urls), path("", app.urls)]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)