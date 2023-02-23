"""Defines URL patterns for learning_logs"""

from django.urls import path
from . import views

app_name = 'ui_app'
urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    path('api/files/<int:receipt_id>', views.api, name='api'),
    path('receipt/<int:receipt_id>', views.receipt, name='receipt'),
]
