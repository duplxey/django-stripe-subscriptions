# Setting up Stripe subscriptions with Django

## Want to learn how to build this?

Check out the [post](https://testdriven.io/blog/django-stripe-subscriptions/).

## Want to use this project?

1. Fork/Clone

1. Create and activate a virtual environment:

    ```sh
    $ python3 -m venv venv && source venv/bin/activate
    ```

1. Install the requirements:

    ```sh
    (venv)$ pip install -r requirements.txt
    ```

1. Apply the migrations:

    ```sh
    (venv)$ python manage.py migrate
    ```

1. Add your Stripe test secret key, test publishable key, endpoint secret and price API ID to the *settings.py* file:

    ```python
    STRIPE_PUBLISHABLE_KEY = '<your test publishable key here>'
    STRIPE_SECRET_KEY = '<your test secret key here>'
    STRIPE_PRICE_ID = '<your price api id here>'
    STRIPE_ENDPOINT_SECRET = '<your endpoint secret here>'
    ```

1. Run the server:

    ```sh
    (venv)$ python manage.py runserver
    ```
