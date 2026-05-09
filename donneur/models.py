from django.db import models
from accounts.models import Donneur


class ReponseAppel(models.Model):
    demande = models.ForeignKey('hopital.DemandeUrgente', on_delete=models.CASCADE, related_name='reponses')
    donneur = models.ForeignKey(Donneur, on_delete=models.CASCADE)
    date_reponse = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, default='En attente')

    class Meta:
        unique_together = ('demande', 'donneur')

    def __str__(self):
        return f"{self.donneur} → {self.demande}"
