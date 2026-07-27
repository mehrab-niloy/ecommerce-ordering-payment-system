from django.contrib import admin

# Register your models here.
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "provider",
        "status",
        "transaction_id",
        "created_at",
    )

    search_fields = (
        "transaction_id",
    )

    list_filter = (
        "provider",
        "status",
    )
