from django.urls import path
from .views import ParseAndStoreCVsView

urlpatterns = [
    path('parse-store-cvs/', ParseAndStoreCVsView.as_view(), name='parse-store-cvs'),
]
