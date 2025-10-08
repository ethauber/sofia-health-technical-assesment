import json

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

import stripe

from .models import Appointment
from .forms import AppointmentForm

stripe.api_key = settings.STRIPE_SECRET_KEY


def appointment_form_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save()
            # return render(
            #     request, 'success.html',
            #     {'appointment': appointment}
            # )
            return redirect('payment_checkout', appointment_id=appointment.id)
    else:
        form = AppointmentForm()
    return render(request, 'book_appointment.html', {'form': form})


def payment_checkout(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'payment_checkout.html', {
        'appointment': appointment,
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'appointment_price': settings.APPOINTMENT_PRICE
    })


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

@method_decorator(csrf_exempt, name='dispatch')
class CreateCheckoutSessionView(View):
    def post(self, request, appointment_id):
        try:
            appointment = get_object_or_404(Appointment, id=appointment_id)

            # Create Stripe checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f'Appointment with {appointment.provider_name}',
                            'description': f'Appointment with {appointment.provider_name}'
                            f' on {appointment.appointment_time}',
                        },
                        'unit_amount': settings.APPOINTMENT_PRICE * 100,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri(
                    f'/appointments/payment/success/{appointment_id}/'),
                cancel_url=request.build_absolute_uri(
                    f'/appointments/payment/cancel/{appointment_id}/'),
                metadata={
                    'appointment_id': appointment_id,
                    'provider_name': appointment.provider_name,
                    'client_email': appointment.client_email
                },
            )
            return JsonResponse({
                'success': True,
                'message': 'Checkout session created successfully',
                'checkout_url': checkout_session.url
            }, status=200)
        except Exception as e:
            return JsonResponse({
                'success': False, 'message': str(e)
            }, status=500)


def payment_success(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    return render(request, 'payment_success.html', {
        'appointment': appointment
    })


def payment_cancel(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    return render(request, 'payment_cancel.html', {
        'appointment': appointment
    })
