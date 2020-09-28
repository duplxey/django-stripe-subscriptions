# django-stripe-subscriptions
- dotenv
- accounts url register file
- stripe_product_id -> stripe_price_id
- remove stripe from success, cancel
- just subscribed message!

## Setup
1. Visit Stripe dashboard and create a new product with 'Recurring' payment.
1. Create a new virtual environment (https://docs.python.org/3/tutorial/venv.html).
1. Create a new `.env` file (in this directory) containing the following:
    ```
    STRIPE_PUBLISHABLE_KEY = '<your publishable key>'
    STRIPE_SECRET_KEY = '<your stripe secret key>'
    STRIPE_ENDPOINT_SECRET = '<your endpoint secret key>'
    STRIPE_PRODUCT_ID = '<your product api id (from product created in the first step)>'
    ```
1. Install the packages in requirements.txt (`pip install -r requirements.txt`).
1. Run the migrations (`python manage.py migrate`).
1. Run the server (`python manage.py runserver`)!
1. Register your webhook on Stripe Dashboard or forward events using Stripe CLI.
