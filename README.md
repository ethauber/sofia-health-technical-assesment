# a59ae98d8bf64c45a0c306ff2541f5e6
# Purpose
To build a simple Django app that demonstrates the use of Django and Stripe.
It will create the following:
 - A model for Appointments with fields provider_name, appointment_time, and client_email.
 - A form along with API endpoint to create an appointment.
 - A mock payment flow using Stripe test keys to show the creation of a test payment checkout session.

##  Initial Setup
### Setup and install dependencies
```
pyenv local 3.11.8
python -m venv env
source env/bin/activate
pip install -r requirements.in
pip freeze > requirements.txt
```

### Create a new project with a new app
```
mkdir sofia-health
django-admin startproject rootsite sofia-health
cd sofia-health
python manage.py startapp appointments
```

### Run the server
python manage.py runserver
