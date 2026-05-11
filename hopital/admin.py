from django.contrib import admin
from .models import DemandeUrgente, Campagne, Creneau, InscriptionCampagne

@admin.register(DemandeUrgente)
class DemandeUrgenteAdmin(admin.ModelAdmin):
    list_display = ('hopital', 'groupe_sanguin', 'quantite', 'statut', 'date_publication')
    list_filter = ('statut', 'groupe_sanguin', 'date_publication')
    search_fields = ('hopital__nom', 'description')
    readonly_fields = ('date_publication',)
    fieldsets = (
        ('Informations de la demande', {
            'fields': ('hopital', 'groupe_sanguin', 'quantite')
        }),
        ('Détails', {
            'fields': ('description', 'delai', 'statut')
        }),
        ('Dates', {
            'fields': ('date_publication',)
        }),
    )


@admin.register(Campagne)
class CampagneAdmin(admin.ModelAdmin):
    list_display = ('nom', 'hopital', 'date_debut', 'date_fin', 'lieu', 'capacite_totale', 'est_active')
    list_filter = ('est_active', 'date_debut', 'hopital')
    search_fields = ('nom', 'lieu', 'hopital__nom')
    readonly_fields = ()
    fieldsets = (
        ('Informations de base', {
            'fields': ('hopital', 'nom', 'description')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin')
        }),
        ('Détails', {
            'fields': ('lieu', 'capacite_totale', 'groupes_cibles', 'est_active')
        }),
    )


@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = ('campagne', 'date', 'heure_debut', 'heure_fin', 'capacite', 'places_restantes')
    list_filter = ('date', 'campagne')
    search_fields = ('campagne__nom',)
    readonly_fields = ()
    
    def places_restantes(self, obj):
        return obj.places_restantes()
    places_restantes.short_description = 'Places restantes'


@admin.register(InscriptionCampagne)
class InscriptionCampagneAdmin(admin.ModelAdmin):
    list_display = ('donneur', 'campagne', 'creneau', 'statut', 'date_inscription', 'present')
    list_filter = ('statut', 'date_inscription', 'present', 'campagne')
    search_fields = ('donneur__user__username', 'campagne__nom')
    readonly_fields = ('date_inscription',)
    fieldsets = (
        ('Inscription', {
            'fields': ('donneur', 'campagne', 'creneau', 'date_inscription')
        }),
        ('Statut', {
            'fields': ('statut', 'present', 'notes')
        }),
    )
