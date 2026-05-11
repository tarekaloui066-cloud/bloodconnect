from django.urls import path
from . import views

app_name = 'hopital'

urlpatterns = [
    path('dashboard/', views.hopital_dashboard, name='dashboard'),
    path('demande/nouvelle/', views.creer_demande, name='creer_demande'),
    path('demande/<int:demande_id>/editer/', views.editer_demande, name='editer_demande'),
    path('demande/<int:demande_id>/cloturer/', views.cloturer_demande, name='cloturer_demande'),
    path('liste/', views.liste_hopitaux, name='liste_hopitaux'),
    path('reponse/<int:reponse_id>/confirmer/', views.confirmer_reponse, name='confirmer_reponse'),
    path('reponse/<int:reponse_id>/refuser/', views.refuser_reponse, name='refuser_reponse'),
    
    # Campagnes
    path('campagnes/', views.gerer_campagnes, name='gerer_campagnes'),
    path('campagne/nouvelle/', views.creer_campagne, name='creer_campagne'),
    path('campagne/<int:campagne_id>/editer/', views.editer_campagne, name='editer_campagne'),
    path('campagne/<int:campagne_id>/', views.detail_campagne, name='detail_campagne'),
    path('campagne/<int:campagne_id>/creneau/ajouter/', views.ajouter_creneau, name='ajouter_creneau'),
    path('creneau/<int:creneau_id>/supprimer/', views.supprimer_creneau, name='supprimer_creneau'),
]