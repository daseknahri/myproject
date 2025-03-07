from django.urls import path

from .admin import revenue_report
from . import views

urlpatterns = [
    path('', views.home, name='register'),
    path('revenue-report/', revenue_report, name='revenue_report'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('api/get-car-daily-rate/', views.get_car_daily_rate, name="get_car_daily_rate"),

]
