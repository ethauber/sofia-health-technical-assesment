from django.db import models
from django.core.validators import validate_email

class Appointment(models.Model):
    provider_name = models.CharField(max_length=255)
    appointment_time = models.DateTimeField()
    client_email = models.EmailField(validators=[validate_email])

    def __str__(self):
        return f"{self.provider_name} - {self.appointment_time}"
