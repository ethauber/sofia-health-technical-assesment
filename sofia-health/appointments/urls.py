from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.appointment_form_view, name='book_appointment'),
    path('api/appointments/', views.AppointmentAPIView.as_view(), name='appointments_api'),
    path('payment/create-checkout-session/<int:appointment_id>/', views.CreateCheckoutSessionView.as_view(), name='create_checkout_session'),
    path('payment/checkout/<int:appointment_id>/', views.payment_checkout, name='payment_checkout'),
    path('payment/success/<int:appointment_id>/', views.payment_success, name='payment_success'),
    path('payment/cancel/<int:appointment_id>/', views.payment_cancel, name='payment_cancel'),
]
