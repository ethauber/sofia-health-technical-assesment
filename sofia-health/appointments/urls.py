from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.appoinment_form_view, name='book_appointment'),
    path('api/appointments/', views.AppointmentAPIView.as_view(), name='appointments_api'),
]
