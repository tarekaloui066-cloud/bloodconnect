from django import forms
from .models import DemandeUrgente, Campagne, Creneau, InscriptionCampagne


class DemandeUrgenteForm(forms.ModelForm):

    class Meta:

        model = DemandeUrgente

        fields = [
            'groupe_sanguin',
            'quantite',
            'delai',
            'description'
        ]

        widgets = {

            'delai': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'description': forms.Textarea(
                attrs={
                    'rows': 4,
                    'placeholder': 'Décrivez le besoin urgent...'
                }
            ),

        }


class CampagneForm(forms.ModelForm):
    class Meta:
        model = Campagne
        fields = ['nom', 'date_debut', 'date_fin', 'lieu', 'groupes_cibles', 'capacite_totale', 'description']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom de la campagne'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'lieu': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Lieu de collecte'}),
            'groupes_cibles': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex: O+, A+, B- (séparés par des virgules)'
            }),
            'capacite_totale': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description...'})
        }


class CreneauForm(forms.ModelForm):
    class Meta:
        model = Creneau
        fields = ['heure_debut', 'heure_fin', 'date', 'capacite']
        widgets = {
            'heure_debut': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'heure_fin': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'capacite': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class InscriptionCampagneForm(forms.ModelForm):
    class Meta:
        model = InscriptionCampagne
        fields = ['creneau']
        widgets = {
            'creneau': forms.Select(attrs={'class': 'form-select'})
        }