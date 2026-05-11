from django.urls import path
from . import views
from hopital import views as hopital_views

app_name = 'donneur'

urlpatterns = [
    path('dashboard/', views.donneur_dashboard, name='dashboard'),
    path('repondre/<int:demande_id>/', views.repondre_appel, name='repondre_appel'),
    path('toggle-actif/', views.toggle_actif, name='toggle_actif'),
    path('enregistrer-don/', views.enregistrer_don, name='enregistrer_don'),

    # Campagnes
    path('campagnes/', hopital_views.lister_campagnes_donneur, name='mes_campagnes'),
    path('campagne/<int:campagne_id>/inscrire/', hopital_views.inscrire_campagne, name='inscrire_campagne'),
    path('inscription/<int:inscription_id>/annuler/', hopital_views.annuler_inscription_campagne, name='annuler_inscription'),
]
