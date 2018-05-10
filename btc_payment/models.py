from __future__ import unicode_literals

from django.db import models
from cartridge.shop.models import Order
import datetime


class BtcInvoice(models.Model):
    """BTC invoice associated with an order."""

    invoice_id = models.CharField(max_length=15)
    address = models.CharField(max_length=100, null=True)
    price_in_usd = models.DecimalField(max_digits=15, decimal_places=8)
    price_in_btc = models.DecimalField(max_digits=15, decimal_places=8)
    added_time = models.DateTimeField(default=datetime.datetime.now)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.invoice_id

    class Meta:
        get_latest_by = "added_time"


class BtcInvoicePayment(models.Model):
    """Used for saving the successful transactions."""

    transaction_hash = models.CharField(max_length=150, null=True)
    value = models.PositiveIntegerField(
        help_text="Must be devided by 100000000 to get the BTC amount."
    )
    invoice = models.OneToOneField(
        BtcInvoice, on_delete=models.CASCADE, null=True
    )


class BtcPendingInvoicePayment(models.Model):
    """Used for saving pending transactions."""

    invoice_id = models.CharField(max_length=15)
    transaction_hash = models.CharField(max_length=150, null=True)
    value = models.PositiveIntegerField(
        help_text="Must be devided by 100000000 to get the BTC amount."
    )
