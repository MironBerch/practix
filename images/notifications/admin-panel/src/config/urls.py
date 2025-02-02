from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('notifications/admin/', admin.site.urls),
]
