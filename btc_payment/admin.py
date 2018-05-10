from django.contrib import admin
from django.shortcuts import reverse
from django.utils.html import format_html
from cartridge.shop.models import Order
from .models import BtcInvoicePayment
from .models import BtcPendingInvoicePayment, BtcInvoice


def get_link(model_to_ink, instance, field):
    """Utility function."""
    info = (model_to_ink._meta.app_label, model_to_ink._meta.model_name)
    if getattr(instance, field):
        attr_id = getattr(instance, field).id
        admin_url = reverse('admin:%s_%s_change' % info, args=(attr_id,))
        return_str = format_html("<a href='{}'>{}</a>", admin_url, field)
    else:
        return_str = 'None'
    return return_str


class BtcPendingInvoicePaymentsAdmin(admin.ModelAdmin):
    list_display = ('invoice_id', 'value')


class BtcInvoiceAdmin(admin.ModelAdmin):
    """Add new column."""

    list_display = (
        'invoice_id',
        'address',
        'price_in_usd',
        'price_in_btc',
        'added_time',
        'order_link'
    )

    def order_link(self, invoice):
        """Link to related Order instance."""
        return get_link(Order, invoice, 'order')
    order_link.short_description = "Related Order"


class BtcInvoicePaymentsAdmin(admin.ModelAdmin):
    """Add 2 new columns to list_display."""

    list_display = ('invoice_id', 'value', 'rel_order', 'rel_btc_invoice')

    def rel_order(self, payment):
        """Link to related Order instabce."""
        if getattr(payment, 'invoice'):
            return get_link(Order, payment.invoice, 'order')
    rel_order.short_description = "Related Order"

    def rel_btc_invoice(self, payment):
        """Link to related BtcInvoice instance."""
        return get_link(BtcInvoice, payment, 'invoice')
    rel_btc_invoice.short_description = "Related Invoice"


admin.site.register(BtcInvoicePayment, BtcInvoicePaymentsAdmin)
admin.site.register(BtcPendingInvoicePayment, BtcPendingInvoicePaymentsAdmin)
admin.site.register(BtcInvoice, BtcInvoiceAdmin)
