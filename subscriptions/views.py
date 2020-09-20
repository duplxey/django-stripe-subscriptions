import stripe
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from djangostripesubs import settings
from djangostripesubs.settings import STRIPE_PRODUCT_ID
from subscriptions.models import StripeCustomer


class HomePageView(TemplateView):
    template_name = 'home.html'


class SuccessView(TemplateView):
    template_name = 'success.html'


class CancelView(TemplateView):
    template_name = 'cancel.html'


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - lets capture the payment later
            # [customer_email] - lets you prefill the email input in the form
            # For full details see https:#stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                client_reference_id=request.user.id if request.user.is_authenticated else None,
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='subscription',
                line_items=[
                    {
                        'price': STRIPE_PRODUCT_ID,
                        'quantity': 1,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_ENDPOINT_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']

        client_reference_id = session.get('client_reference_id')
        stripe_customer_id = session.get('customer')

        user = User.objects.get(id=client_reference_id)
        StripeCustomer.objects.create(user=user, stripeCustomerId=stripe_customer_id)

        # Our StripeUser is not authenticated with our authentication User

        print("session")
        print(vars(session))

        # you can fetch customer, subscription, payment method from the session object
        # example data:
        # {
        #     '_unsaved_values': set(),
        #     '_transient_values': set(),
        #     '_last_response': None,
        #     '_retrieve_params': {},
        #     '_previous': OrderedDict([
        #         ('id',
        #          'cs_test_qXrHUwPkf1Gjjx7IzCOMlbZj015KkgcJGF5FAMnUORCF1owjxjHvUFQY'
        #          ),
        #         ('object', 'checkout.session'),
        #         ('allow_promotion_codes', None),
        #         ('amount_subtotal', 500),
        #         ('amount_total', 500),
        #         ('billing_address_collection', None),
        #         ('cancel_url', 'http://localhost:8000/cancelled/'),
        #         ('client_reference_id', None),
        #         ('currency', 'eur'),
        #         ('customer', 'cus_I3MbTLnHXTKFDP'),
        #         ('customer_email', None),
        #         ('livemode', False),
        #         ('locale', None),
        #         ('metadata', OrderedDict()),
        #         ('mode', 'subscription'),
        #         ('payment_intent', None),
        #         ('payment_method_types', ['card']),
        #         ('payment_status', 'paid'),
        #         ('setup_intent', None),
        #         ('shipping', None),
        #         ('shipping_address_collection', None),
        #         ('submit_type', None),
        #         ('subscription', 'sub_I3MbYgV7COHt1z'),
        #         ('success_url',
        #          'http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}'
        #          ),
        #         ('total_details', OrderedDict([('amount_discount', 0),
        #                                        ('amount_tax', 0)])),
        #     ]),
        #     'api_key': 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        #     'stripe_version': None,
        #     'stripe_account': None,
        # }

        # TODO: make changes to our models

    return HttpResponse(status=200)
