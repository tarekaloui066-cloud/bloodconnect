from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .forms import DonneurProfileForm
from .models import ReponseAppel, Don
from hopital.models import DemandeUrgente


@login_required
def repondre_appel(request, demande_id):
    demande = get_object_or_404(DemandeUrgente, id=demande_id)
    try:
        donneur = request.user.donneur

        # Bloquer si compte désactivé
        if not donneur.actif:
            messages.error(request, "⛔ Votre compte est désactivé. Réactivez-le pour répondre aux appels urgents.")
            return redirect('home')

        if donneur.groupe_sanguin != demande.groupe_sanguin:
            messages.error(request, "Désolé, votre groupe sanguin n'est pas compatible avec cette demande.")
            return redirect('home')

        # Vérifier l'éligibilité (56j/84j)
        historique_dons = Don.objects.filter(donneur=donneur).order_by('-date_don')
        dernier_don = historique_dons.first()
        est_eligible = True
        prochaine_date_eligible = None

        if dernier_don:
            prochaine_date_eligible = dernier_don.prochaine_date_eligibilite()
            est_eligible = timezone.now().date() >= prochaine_date_eligible

        if not est_eligible:
            messages.error(
                request,
                f"❌ Vous ne pouvez pas donner avant le {prochaine_date_eligible.strftime('%d/%m/%Y')}. "
                f"Selon votre sexe, vous devez attendre {56 if donneur.sexe == 'M' else 84} jours entre chaque don."
            )
            return redirect('home')

        # Créer la réponse
        reponse, created = ReponseAppel.objects.get_or_create(
            demande=demande,
            donneur=donneur
        )
        if created:
            messages.success(request, "✓ Votre intention de don a été enregistrée. L'hôpital vous contactera prochainement.")
        else:
            messages.info(request, "Vous avez déjà répondu à cet appel urgent.")

    except AttributeError:
        messages.warning(request, "Cette action est réservée aux comptes donneurs.")

    return redirect('home')


@login_required
def toggle_actif(request):
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    if request.method == 'POST':
        donneur.actif = not donneur.actif
        donneur.save()
        if donneur.actif:
            messages.success(request, "✓ Votre compte est maintenant actif. Vous apparaissez dans les recherches.")
        else:
            messages.warning(request, "⏸ Votre compte est temporairement désactivé. Vous n'apparaîtrez plus dans les appels urgents.")
    return redirect('donneur:dashboard')


@login_required
def donneur_dashboard(request):
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    if request.method == 'POST':
        form = DonneurProfileForm(request.POST, request.FILES, instance=donneur)
        if form.is_valid():
            form.save()
            messages.success(request, "Profil mis à jour avec succès !")
            return redirect('donneur:dashboard')
    else:
        form = DonneurProfileForm(instance=donneur)

    historique_dons = Don.objects.filter(donneur=donneur)

    dernier_don = historique_dons.first()
    prochaine_date = None
    est_eligible = True
    if dernier_don:
        prochaine_date = dernier_don.prochaine_date_eligibilite()
        est_eligible = timezone.now().date() >= prochaine_date

    appels_compatibles = DemandeUrgente.objects.filter(
        groupe_sanguin=donneur.groupe_sanguin,
        statut='active',
        hopital__est_valide=True
    ).select_related('hopital').order_by('-date_publication')

    mes_reponses = ReponseAppel.objects.filter(donneur=donneur).select_related('demande__hopital').order_by('-date_reponse')
    reponses_ids = set(mes_reponses.values_list('demande_id', flat=True))

    # Campagnes inscrites
    from hopital.models import InscriptionCampagne
    mes_inscriptions_campagne = InscriptionCampagne.objects.filter(
        donneur=donneur
    ).select_related('campagne__hopital', 'creneau').order_by('campagne__date_debut')

    return render(request, 'donneur/donneur_dashboard.html', {
        'form': form,
        'donneur': donneur,
        'historique_dons': historique_dons,
        'dernier_don': dernier_don,
        'prochaine_date': prochaine_date,
        'est_eligible': est_eligible,
        'appels_compatibles': appels_compatibles,
        'mes_reponses': mes_reponses,
        'reponses_ids': reponses_ids,
        'mes_inscriptions_campagne': mes_inscriptions_campagne,
    })

@login_required
def enregistrer_don(request):
    """Permet au donneur d'enregistrer manuellement un don."""
    try:
        donneur = request.user.donneur
    except AttributeError:
        return redirect('home')

    if request.method == 'POST':
        from .forms import DonForm
        form = DonForm(request.POST)
        if form.is_valid():
            don = form.save(commit=False)
            don.donneur = donneur
            don.save()
            messages.success(request, "✓ Don enregistré avec succès.")
            return redirect('donneur:dashboard')
    else:
        from .forms import DonForm
        form = DonForm()

    return render(request, 'donneur/enregistrer_don.html', {'form': form})
