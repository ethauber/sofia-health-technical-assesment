from django.test import TestCase
from .models import Appointment


class AppointmentModelTest(TestCase):
    def test_str_representation(self):
        appointment = Appointment(
            provider_name="John Doe",
            appointment_time="2025-10-01 10:00:00+00:00",
            client_email="john.doe@example.com"
        )
        self.assertEqual(appointment.provider_name, "John Doe")
        self.assertEqual(
            appointment.appointment_time, "2025-10-01 10:00:00+00:00")
        self.assertEqual(appointment.client_email, "john.doe@example.com")

        self.assertEqual(Appointment.objects.count(), 0)
        appointment.save()
        self.assertEqual(Appointment.objects.count(), 1)

