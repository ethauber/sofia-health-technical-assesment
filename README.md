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


## Part 2
If this appointment feature had to handle thousands of requests per day the changes that I would address are to setup the application to run in the AWS environment, or preferred cloud provider like Azure or GCP.

To do this I would first ensure that the database is configured to a platform as a service, or managed database service, like AWS RDS, Azure Database for PostgreSQL, or Google Cloud SQL (Spanner if Global scale is required). Then after this I would look to run this Django application on AWS ECS containers or equivalent on the preferred cloud provider so that the application can scale horizontally and handle the projected amount of requests. By making these first two changes the application will be more resilient to high traffic and more reliable.

I would communicate progress through ongoing slack updates, or the preferred messaging app by the company. In these updates I would likely often include screenshots and/or video recordings. When communicating with a non-technical team member include similies or metaphors where I can and keep it simple and to the point. Blockers would be communicated with their impact, what options are available to resolve the blocker, and my personal recommendation.
