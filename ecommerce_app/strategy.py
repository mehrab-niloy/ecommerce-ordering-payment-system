from abc import ABC, abstractmethod

from .services.stripe_service import StripePaymentService


class PaymentStrategy(ABC):
    """
    Abstract Base Class for all payment providers.
    """

    @abstractmethod
    def create_payment(self, order):
        pass


class StripeStrategy(PaymentStrategy):
    """
    Stripe payment implementation.
    """

    def create_payment(self, order):
        service = StripePaymentService()
        return service.create_payment_intent(order)


class BkashStrategy(PaymentStrategy):
    """
    Placeholder for future bKash implementation.
    """

    def create_payment(self, order):
        raise NotImplementedError("bKash integration is not implemented yet.")