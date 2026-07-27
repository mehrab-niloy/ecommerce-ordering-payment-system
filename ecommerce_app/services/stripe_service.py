import stripe

from django.conf import settings

from ecommerce_app.models import Payment,Order


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripePaymentService:

    def create_payment_intent(self, order):
     """
     Create Stripe PaymentIntent
     """
     try:
        payment_intent = stripe.PaymentIntent.create(
            amount=int(order.total_amount * 100),
            currency="usd",
            metadata={"order_id": order.id},
        )
     except stripe.error.StripeError as e:
        raise Exception(f"Stripe Error: {str(e)}")

     payment = Payment.objects.create(
        order=order,
        provider="stripe",
        transaction_id=payment_intent.id,
        status="pending",
        raw_response=payment_intent.to_dict()   # ✅ Fixed
    )

     return {
        "payment": payment,
        "client_secret": payment_intent.client_secret,
        "payment_intent_id": payment_intent.id,
    }