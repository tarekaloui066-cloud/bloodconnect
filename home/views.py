from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from hopital.models import DemandeUrgente
from accounts.models import Donneur, Hopital
from donneur.models import Don, ReponseAppel
import csv
from django.db.models import Count, Q


def home(request):
    # Afficher uniquement les demandes urgentes des hôpitaux validés
    demandes = DemandeUrgente.objects.filter(
        statut='active',
        hopital__est_valide=True
    ).select_related('hopital').order_by('-date_publication')

    return render(
        request,
        'home.html',
        {'demandes': demandes}
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """Tableau de bord admin avec statistiques."""
    # Compter les donneurs
    total_donneurs = Donneur.objects.count()
    donneurs_actifs = Donneur.objects.filter(actif=True).count()
    
    # Compter les hôpitaux
    total_hopitaux = Hopital.objects.count()
    hopitaux_valides = Hopital.objects.filter(est_valide=True).count()
    
    # Compter les dons
    total_dons = Don.objects.count()
    
    # Demandes urgentes
    demandes_actives = DemandeUrgente.objects.filter(statut='active').count()
    demandes_fermees = DemandeUrgente.objects.filter(statut='fermee').count()
    
    # Demandes par groupe sanguin
    demandes_par_groupe = DemandeUrgente.objects.filter(
        statut='active'
    ).values('groupe_sanguin').annotate(count=Count('id')).order_by('-count')
    
    # Réponses
    total_reponses = ReponseAppel.objects.count()
    reponses_confirmees = ReponseAppel.objects.filter(statut='Confirmé').count()
    
    # Donneurs par groupe sanguin
    donneurs_par_groupe = Donneur.objects.values('groupe_sanguin').annotate(
        count=Count('id')
    ).order_by('-count')

    # Hopitaux en attente de validation
    hopitaux_en_attente = Hopital.objects.filter(est_valide=False).order_by('-date_inscription')
    
    # Demandes par ville
    demandes_par_ville = DemandeUrgente.objects.filter(
        statut="active"
    ).values("hopital__ville").annotate(count=Count("id")).order_by("-count")[:10]

    context = {
        'total_donneurs': total_donneurs,
        'donneurs_actifs': donneurs_actifs,
        'total_hopitaux': total_hopitaux,
        'hopitaux_valides': hopitaux_valides,
        'total_dons': total_dons,
        'demandes_actives': demandes_actives,
        'demandes_fermees': demandes_fermees,
        'demandes_par_groupe': demandes_par_groupe,
        'total_reponses': total_reponses,
        'reponses_confirmees': reponses_confirmees,
        'donneurs_par_groupe': donneurs_par_groupe,
        'hopitaux_en_attente': hopitaux_en_attente,
        'demandes_par_ville': demandes_par_ville,
    }

    return render(request, 'admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def export_donneurs_csv(request):
    """Exporte la liste des donneurs en CSV."""
    donneurs = Donneur.objects.select_related('user').all()

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="donneurs.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nom d\'utilisateur', 'Email', 'Groupe sanguin', 'Sexe', 'Date de naissance', 'Ville', 'Téléphone', 'Actif'])

    for donneur in donneurs:
        writer.writerow([
            donneur.user.username,
            donneur.user.email,
            donneur.groupe_sanguin,
            donneur.get_sexe_display(),
            donneur.date_naissance,
            donneur.ville,
            donneur.telephone,
            'Oui' if donneur.actif else 'Non'
        ])

    return response

@login_required
@user_passes_test(lambda u: u.is_staff)
def valider_hopital(request, hopital_id):
    """Valide un hôpital en attente."""
    hopital = get_object_or_404(Hopital, id=hopital_id)
    hopital.est_valide = True
    hopital.save()
    messages.success(request, f"✓ Hôpital '{hopital.nom}' validé.")
    return redirect('admin_dashboard')


@login_required
@user_passes_test(lambda u: u.is_staff)
def rejeter_hopital(request, hopital_id):
    """Rejette/désactive un hôpital."""
    hopital = get_object_or_404(Hopital, id=hopital_id)
    hopital.est_valide = False
    hopital.save()
    messages.warning(request, f"Hôpital '{hopital.nom}' désactivé.")
    return redirect('admin_dashboard')
