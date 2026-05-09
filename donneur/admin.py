from django.contrib import admin
from .models import ReponseAppel

@admin.register(ReponseAppel)
class ReponseAppelAdmin(admin.ModelAdmin):
    list_display = ('demande', 'donneur', 'statut', 'date_reponse')
    list_filter = ('statut', 'date_reponse')
    search_fields = ('demande__hopital__nom', 'donneur__user__username')
    readonly_fields = ('date_reponse',)
