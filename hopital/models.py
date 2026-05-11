from django.db import models
from accounts.models import Hopital


class DemandeUrgente(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='demandes')
    groupe_sanguin = models.CharField(max_length=5)
    quantite = models.IntegerField(help_text="Nombre de poches")
    delai = models.DateField()
    statut = models.CharField(max_length=20, default='active')
    description = models.TextField(blank=True)
    date_publication = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.groupe_sanguin} - {self.hopital.nom}"


class Campagne(models.Model):
    hopital = models.ForeignKey(Hopital, on_delete=models.CASCADE, related_name='campagnes')
    nom = models.CharField(max_length=200)
    date_debut = models.DateField()
    date_fin = models.DateField()
    lieu = models.CharField(max_length=255)
    groupes_cibles = models.CharField(
        max_length=100,
        help_text="Ex: O+, A+, B- (séparés par des virgules)",
        blank=True
    )
    capacite_totale = models.IntegerField(default=100, help_text="Nombre total de donneurs possibles")
    description = models.TextField(blank=True)
    est_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_debut']

    def __str__(self):
        return f"{self.nom} - {self.hopital.nom}"

    def places_restantes(self):
        """Calcule le nombre de places restantes."""
        total_inscrits = InscriptionCampagne.objects.filter(campagne=self).count()
        return self.capacite_totale - total_inscrits

    def est_pleine(self):
        """Vérifie si la campagne est complète."""
        return self.places_restantes() <= 0


class Creneau(models.Model):
    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, related_name='creneaux')
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    capacite = models.IntegerField(default=10)
    date = models.DateField()

    class Meta:
        ordering = ['date', 'heure_debut']
        unique_together = ('campagne', 'date', 'heure_debut')

    def __str__(self):
        return f"{self.campagne.nom} - {self.date} {self.heure_debut}-{self.heure_fin}"

    def places_restantes(self):
        """Calcule le nombre de places disponibles pour ce créneau."""
        total_inscrits = InscriptionCampagne.objects.filter(creneau=self).count()
        return self.capacite - total_inscrits

    def est_plein(self):
        """Vérifie si le créneau est complet."""
        return self.places_restantes() <= 0


class InscriptionCampagne(models.Model):
    STATUT_CHOICES = [
        ('inscrit', 'Inscrit'),
        ('confirme', 'Confirmé'),
        ('absent', 'Absent'),
        ('annule', 'Annulé')
    ]

    campagne = models.ForeignKey(Campagne, on_delete=models.CASCADE, related_name='inscriptions')
    creneau = models.ForeignKey(Creneau, on_delete=models.CASCADE, related_name='inscriptions')
    donneur = models.ForeignKey('accounts.Donneur', on_delete=models.CASCADE, related_name='inscriptions_campagne')
    date_inscription = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='inscrit')
    present = models.BooleanField(default=False, help_text="Indicateur de présence le jour J")
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('campagne', 'donneur')
        ordering = ['-date_inscription']

    def __str__(self):
        return f"{self.donneur.user.username} - {self.campagne.nom}"
