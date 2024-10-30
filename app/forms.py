from django import forms
from .models import Reservation

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_time', 'end_time'] 
        widgets = {
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                }),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        # Vérification de la validité des heures
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError("L'heure de fin doit être supérieure à l'heure de début.")

        return cleaned_data
