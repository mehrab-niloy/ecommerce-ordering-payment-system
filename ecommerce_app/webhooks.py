import stripe

from django.conf import settings
from django.db import transaction
from django.db.models import F
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from ecommerce_app.models import OrderItem, Payment, Product

stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):

    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=settings.STRIPE_WEBHOOK_SECRET,
        )

    except ValueError:
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # ==================================================
    # PAYMENT SUCCESS
    # ==================================================

    if event["type"] == "payment_intent.succeeded":

        payment_intent = event["data"]["object"]
        transaction_id = payment_intent["id"]

        try:
            with transaction.atomic():

                payment = Payment.objects.select_for_update().get(
                    transaction_id=transaction_id
                )

                # Prevent duplicate webhook processing
                if payment.status == "success":
                    return HttpResponse(status=200)

                payment.status = "success"
                payment.raw_response = payment_intent.to_dict()
                payment.save(update_fields=["status", "raw_response"])

                order = payment.order

                # Lock all order items with their products
                order_items = (
                    OrderItem.objects
                    .select_related("product")
                    .filter(order=order)
                )

                for item in order_items:

                    product = Product.objects.select_for_update().get(
                        id=item.product.id
                    )

                    # Double-check stock
                    if product.stock < item.quantity:
                        return HttpResponse(
                            f"Insufficient stock for {product.product_name}",
                            status=400
                        )

                    # Atomic stock reduction
                    Product.objects.filter(id=product.id).update(
                        stock=F("stock") - item.quantity
                    )

                order.status = "paid"
                order.save(update_fields=["status"])

        except Payment.DoesNotExist:
            return HttpResponse(status=404)

    # ==================================================
    # PAYMENT FAILED
    # ==================================================

    elif event["type"] == "payment_intent.payment_failed":

        payment_intent = event["data"]["object"]
        transaction_id = payment_intent["id"]

        try:

            payment = Payment.objects.get(
                transaction_id=transaction_id
            )

            payment.status = "failed"
            payment.raw_response = payment_intent.to_dict()
            payment.save(update_fields=["status", "raw_response"])

        except Payment.DoesNotExist:
            pass

    return HttpResponse(status=200)