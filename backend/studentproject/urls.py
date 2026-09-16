"""
Root URL configuration for studentproject.
This file connects incoming URLs to the correct app.
"""

from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    # Student CRUD API
    path('api/students/', include('students.urls')),
]
