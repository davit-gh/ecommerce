from btc_payment.models import BtcInvoice


def payment_handler(request, order_form, order):
    """
    Called after a successful payment.

    Associates an order with the respective BtcInvoice object
    for display in admin UI.

    """
    invoice_id = request.POST.get('invoice_id')
    invoice = BtcInvoice.objects.filter(invoice_id=invoice_id).first()
    if invoice:
        invoice.order = order
        invoice.save()
    return invoice_id
