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

### Create and run migration for new appointments model
```
python manage.py makemigrations appointments
python manage.py migrate
```

#### Test for the model
```
python manage.py test appointments
```

### Retrieve stripe keys
Signup for a stripe account and retrieve the publishable and secret keys.
```
export STRIPE_PUBLISHABLE_KEY=<your_publishable_key>
export STRIPE_SECRET_KEY=<your_secret_key>
```

### Run the server
```
python manage.py runserver
```

## Stripe integration explanation
The customer fills out the appointment form and submits it. After submitting the appointment form the customer is then redirected to the payment page with the appointment details. At this point the customer then clicks the pay with stripe button and is redirected to the stripe checkout page. The customer then either enters valid payment and pays the fee or cancels the payment. Depending on the customer's choice, the customer is redirected to the designated success or cancel page.
  
### Test cards included here for convenience
- Success: 4242 4242 4242 4242
- Declined: 4000 0000 0000 0002
