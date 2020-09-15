import random

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from subscriptions.models import StripeCustomer


@receiver(post_save, sender=User)
def on_user_create(sender, instance, created, raw, using, **kwargs):
    if created:
        StripeCustomer.objects.create(user=instance, stripeCustomerId=random.randint(1, 1000))
