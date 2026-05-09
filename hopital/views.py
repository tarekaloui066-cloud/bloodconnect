from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import Hopital
from hopital.models import DemandeUrgente
from hopital.forms import DemandeUrgenteForm
from django.db.models import Q


@login_required
def hopital_dashboard(request):
    try:
        hopital = Hopital.objects.get(user=request.user)
    except Hopital.DoesNotExist:
        return redirect('accounts:login')

    # If not yet approved, show waiting page
    if not hopital.est_valide:
        return render(request, 'hopital/hopital_en_attente.html', {'hopital': hopital})

    demandes = hopital.demandes.all().order_by('-date_publication')
    demandes_actives = demandes.filter(statut='active').count()
    total_demandes = demandes.count()

    return render(request, 'hopital/hopital_dashboard.html', {
        'demandes': demandes,
        'demandes_actives': demandes_actives,
        'total_demandes': total_demandes,
        'hopital': hopital,
    })


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
