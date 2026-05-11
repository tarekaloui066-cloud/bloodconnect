from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
from accounts.models import Hopital, Donneur
from hopital.models import DemandeUrgente, Campagne, Creneau, InscriptionCampagne
from hopital.forms import DemandeUrgenteForm, CampagneForm, CreneauForm, InscriptionCampagneForm
from donneur.models import ReponseAppel, Don


@login_required
def hopital_dashboard(request):
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    if not hopital.est_valide:
        return render(request, 'hopital/hopital_en_attente.html', {'hopital': hopital})

    demandes = hopital.demandes.all().order_by('-date_publication')
    demandes_actives = demandes.filter(statut='active').count()
    total_demandes = demandes.count()

    # Réponses en attente de confirmation pour cet hôpital
    reponses_en_attente = ReponseAppel.objects.filter(
        demande__hopital=hopital,
        statut='En attente'
    ).select_related('donneur__user', 'demande').order_by('-date_reponse')

    return render(request, 'hopital/hopital_dashboard.html', {
        'demandes': demandes,
        'demandes_actives': demandes_actives,
        'total_demandes': total_demandes,
        'hopital': hopital,
        'reponses_en_attente': reponses_en_attente,
    })


@login_required
def confirmer_reponse(request, reponse_id):
    """Confirme une réponse → crée automatiquement un Don."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    reponse = get_object_or_404(ReponseAppel, id=reponse_id, demande__hopital=hopital)

    # Créer le don automatiquement
    don, created = Don.objects.get_or_create(
        donneur=reponse.donneur,
        date_don=timezone.now().date(),
        etablissement=hopital.nom,
        defaults={'notes': f"Don suite à l'appel urgent #{reponse.demande.id}"}
    )

    reponse.statut = 'Confirmé'
    reponse.save()

    messages.success(
        request,
        f"✓ Don de {reponse.donneur.user.username} confirmé et enregistré automatiquement."
    )
    return redirect('hopital:dashboard')


@login_required
def refuser_reponse(request, reponse_id):
    """Refuse une réponse de donneur."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    reponse = get_object_or_404(ReponseAppel, id=reponse_id, demande__hopital=hopital)
    reponse.statut = 'Refusé'
    reponse.save()

    messages.info(request, f"Réponse de {reponse.donneur.user.username} refusée.")
    return redirect('hopital:dashboard')


@login_required
def creer_demande(request):
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    if not hopital.est_valide:
        return redirect('hopital:dashboard')

    if request.method == "POST":
        form = DemandeUrgenteForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.hopital = hopital
            demande.statut = 'active'
            demande.save()
            return redirect('hopital:dashboard')
    else:
        form = DemandeUrgenteForm()

    return render(request, 'hopital/creer_demande.html', {'form': form})


@login_required
def editer_demande(request, demande_id):
    """Éditer une demande urgente existante."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    demande = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)

    if demande.statut == 'fermee':
        messages.error(request, "Impossible de modifier une demande fermée.")
        return redirect('hopital:dashboard')

    if request.method == "POST":
        form = DemandeUrgenteForm(request.POST, instance=demande)
        if form.is_valid():
            form.save()
            messages.success(request, "✓ Demande urgente mise à jour avec succès.")
            return redirect('hopital:dashboard')
    else:
        form = DemandeUrgenteForm(instance=demande)

    return render(request, 'hopital/editer_demande.html', {'form': form, 'demande': demande})


@login_required
def cloturer_demande(request, demande_id):
    """Clôturer une demande urgente."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    demande = get_object_or_404(DemandeUrgente, id=demande_id, hopital=hopital)

    if request.method == "POST":
        demande.statut = 'fermee'
        demande.save()
        messages.success(request, "✓ Demande urgente fermée.")
        return redirect('hopital:dashboard')

    return render(request, 'hopital/confirmer_cloture.html', {'demande': demande})


def liste_hopitaux(request):
    query = request.GET.get('q')
    if query:
        hopitaux = Hopital.objects.filter(
            Q(nom__icontains=query) | Q(ville__icontains=query),
            est_valide=True
        )
    else:
        hopitaux = Hopital.objects.filter(est_valide=True)

    return render(request, 'hopital/liste.html', {'hopitaux': hopitaux, 'query': query or ''})


# ========== VUES CAMPAGNES ==========

@login_required
def gerer_campagnes(request):
    """Liste des campagnes de l'hôpital."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    campagnes = hopital.campagnes.all().order_by('-date_debut')
    return render(request, 'hopital/gerer_campagnes.html', {'campagnes': campagnes, 'hopital': hopital})


@login_required
def creer_campagne(request):
    """Créer une nouvelle campagne de collecte."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    if request.method == 'POST':
        form = CampagneForm(request.POST)
        if form.is_valid():
            campagne = form.save(commit=False)
            campagne.hopital = hopital
            campagne.save()
            messages.success(request, "✓ Campagne créée avec succès.")
            return redirect('hopital:gerer_campagnes')
    else:
        form = CampagneForm()

    return render(request, 'hopital/creer_campagne.html', {'form': form})


@login_required
def editer_campagne(request, campagne_id):
    """Modifier une campagne."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    campagne = get_object_or_404(Campagne, id=campagne_id, hopital=hopital)

    if request.method == 'POST':
        form = CampagneForm(request.POST, instance=campagne)
        if form.is_valid():
            form.save()
            messages.success(request, "✓ Campagne mise à jour.")
            return redirect('hopital:gerer_campagnes')
    else:
        form = CampagneForm(instance=campagne)

    return render(request, 'hopital/editer_campagne.html', {'form': form, 'campagne': campagne})


@login_required
def detail_campagne(request, campagne_id):
    """Détails d'une campagne avec gestion des crénaux."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    campagne = get_object_or_404(Campagne, id=campagne_id, hopital=hopital)
    creneaux = campagne.creneaux.all()
    inscriptions = campagne.inscriptions.all().select_related('donneur', 'creneau')

    return render(request, 'hopital/detail_campagne.html', {
        'campagne': campagne,
        'creneaux': creneaux,
        'inscriptions': inscriptions,
    })


@login_required
def ajouter_creneau(request, campagne_id):
    """Ajouter un créneau à une campagne."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    campagne = get_object_or_404(Campagne, id=campagne_id, hopital=hopital)

    if request.method == 'POST':
        form = CreneauForm(request.POST)
        if form.is_valid():
            creneau = form.save(commit=False)
            creneau.campagne = campagne
            creneau.save()
            messages.success(request, "✓ Créneau ajouté.")
            return redirect('hopital:detail_campagne', campagne_id=campagne.id)
    else:
        form = CreneauForm()

    return render(request, 'hopital/ajouter_creneau.html', {'form': form, 'campagne': campagne})


@login_required
def supprimer_creneau(request, creneau_id):
    """Supprimer un créneau."""
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    creneau = get_object_or_404(Creneau, id=creneau_id, campagne__hopital=hopital)
    campagne_id = creneau.campagne.id
    creneau.delete()
    messages.success(request, "✓ Créneau supprimé.")
    return redirect('hopital:detail_campagne', campagne_id=campagne_id)


@login_required
def lister_campagnes_donneur(request):
    """Afficher les campagnes disponibles pour un donneur."""
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    campagnes_disponibles = Campagne.objects.filter(
        est_active=True,
        date_fin__gte=timezone.now().date()
    ).exclude(
        inscriptions__donneur=donneur
    ).select_related('hopital')

    inscriptions = InscriptionCampagne.objects.filter(donneur=donneur).select_related('campagne', 'creneau')

    return render(request, 'donneur/mes_campagnes.html', {
        'campagnes_disponibles': campagnes_disponibles,
        'mes_inscriptions': inscriptions,
        'donneur': donneur,
    })


@login_required
def inscrire_campagne(request, campagne_id):
    """S'inscrire à une campagne."""
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    campagne = get_object_or_404(Campagne, id=campagne_id, est_active=True)

    if campagne.est_pleine():
        messages.error(request, "❌ La campagne est complète.")
        return redirect('donneur:mes_campagnes')

    if request.method == 'POST':
        creneau_id = request.POST.get('creneau_id')
        creneau = get_object_or_404(Creneau, id=creneau_id, campagne=campagne)

        if creneau.est_plein():
            messages.error(request, "❌ Ce créneau est complet.")
            return redirect('donneur:mes_campagnes')

        # Vérifier si déjà inscrit
        if InscriptionCampagne.objects.filter(campagne=campagne, donneur=donneur).exists():
            messages.warning(request, "Vous êtes déjà inscrit à cette campagne.")
            return redirect('donneur:mes_campagnes')

        inscription = InscriptionCampagne.objects.create(
            campagne=campagne,
            creneau=creneau,
            donneur=donneur
        )
        messages.success(request, "✓ Vous êtes inscrit à la campagne.")
        return redirect('donneur:mes_campagnes')

    # Afficher le formulaire de sélection du créneau
    creneaux_disponibles = Creneau.objects.filter(campagne=campagne).exclude(inscriptions__donneur=donneur)
    return render(request, 'donneur/inscrire_campagne.html', {
        'campagne': campagne,
        'creneaux': creneaux_disponibles
    })


@login_required
def annuler_inscription_campagne(request, inscription_id):
    """Annuler l'inscription à une campagne."""
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    inscription = get_object_or_404(InscriptionCampagne, id=inscription_id, donneur=donneur)
    campagne_id = inscription.campagne.id
    inscription.delete()
    messages.success(request, "✓ Inscription annulée.")
    return redirect('donneur:mes_campagnes')