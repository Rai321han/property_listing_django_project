"""
URL patterns for Property app (Web Pages)

These URLs handle the frontend HTML pages.
API endpoints are in api_urls.py
"""

from django.urls import path
from . import views

app_name = "property"

urlpatterns = [
    # Property pages
    path("all/", views.property_list, name="property_list"),
    path("<int:pk>/", views.property_detail, name="property_detail"),
]
