from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import DonneurProfileForm
from .models import ReponseAppel
from hopital.models import DemandeUrgente


@login_required
def repondre_appel(request, demande_id):
    demande = get_object_or_404(DemandeUrgente, id=demande_id)

    try:
        donneur = request.user.donneur

        if donneur.groupe_sanguin != demande.groupe_sanguin:
            messages.error(request, "Désolé, votre groupe sanguin n'est pas compatible avec cette demande.")
            return redirect('home')

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

    # Get donor's donation responses
    mes_reponses = ReponseAppel.objects.filter(donneur=donneur).select_related('demande__hopital').order_by('-date_reponse')

    return render(request, 'donneur/donneur_dashboard.html', {
        'form': form,
        'donneur': donneur,
        'mes_reponses': mes_reponses,
    })
