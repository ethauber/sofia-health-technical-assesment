import json

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

from .models import Appointment
from .forms import AppointmentForm


def appoinment_form_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            return render(
                request, 'success.html',
                {'appointment': appointment}
            )
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})


@method_decorator(csrf_exempt, name='dispatch')
class AppointmentAPIView(View):

    def post(self, request):
        try:
            data = json.loads(request.body)
            form = AppointmentForm(data=data)

            if form.is_valid():
                appointment = form.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Appointment created successfully',
                    'appointment': {
                        'id': appointment.id,
                        'provider_name': appointment.provider_name,
                        'appointment_time': appointment.appointment_time,
                        'client_email': appointment.client_email
                    }
                }, status=201)
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Invalid form',
                    'errors': form.errors
                }, status=400)
        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'message': 'Invalid JSON',
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False, 'message': str(e)
            }, status=500)
    
    def get(self, request):
        appointments = Appointment.objects.all()
        appointments_data = []
        for appointment in appointments:
            appointments_data.append({
                'id': appointment.id,
                'provider_name': appointment.provider_name,
                'appointment_time': appointment.appointment_time,
                'client_email': appointment.client_email
            })
        return JsonResponse({
            'success': True,
            'message': 'Appointments fetched successfully',
            'appointments': appointments_data
        }, status=200)
