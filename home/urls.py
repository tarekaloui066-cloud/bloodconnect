from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('export/donneurs/', views.export_donneurs_csv, name='export_donneurs_csv'),
    path('admin/hopital/<int:hopital_id>/valider/', views.valider_hopital, name='valider_hopital'),
    path('admin/hopital/<int:hopital_id>/rejeter/', views.rejeter_hopital, name='rejeter_hopital'),
]
