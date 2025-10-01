from django import forms
from django.utils import timezone

from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['provider_name', 'appointment_time', 'client_email']
        widgets = {
            'provider_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter provider name (e.g. Dr. Neo)',
            }),
            'appointment_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'min': timezone.now().strftime('%Y-%m-%dT%H:%M'),
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
            }),
        }

    def clean_appointment_time(self):
        appointment_time = self.cleaned_data['appointment_time']
        if appointment_time <= timezone.now():
            raise forms.ValidationError("Appointment time must be in the future.")
        return appointment_time
