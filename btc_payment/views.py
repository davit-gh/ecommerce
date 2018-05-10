import datetime, pytz
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.http import HttpResponseServerError
from django.http import HttpResponseBadRequest
from django.urls import reverse
from blockchain.blockexplorer import get_address
from blockchain.v2.receive import receive
from mezzanine.conf import settings
from .models import BtcInvoice, BtcInvoicePayment
from .models import BtcPendingInvoicePayment


def _create_callback_url(request, invoice_id, secret):
    relative_url = reverse("payment_handler", args=[invoice_id, secret])
    callback_url = request.build_absolute_uri(relative_url)
    return callback_url


def create_handler(request, order_total, btc_total):
    """
    Create a new bitcoin address if the latest created one has received funds.

    Otherwise use the latest address. The aim is to avoid 'address gap' issue.
    invoice_id should be something unique for the transaction.
    """
    invoice_id = str(request.cart.id)
    recv = BtcInvoice.objects.latest()
    address = recv.address
    received = get_address(address).total_received
    if received > 0:
        callback_url = _create_callback_url(
            request, invoice_id, settings.SECRET_KEY
        )
        recv = receive(settings.XPUB, callback_url, settings.API_KEY)
        address = recv.address
        invoice = BtcInvoice(
            invoice_id=invoice_id,
            price_in_usd=order_total,
            price_in_btc=btc_total,
            address=address
        )
        invoice.save()
    else:
        recv.price_in_usd = order_total
        recv.price_in_btc = btc_total
        recv.added_time = datetime.datetime.now(pytz.utc)
        recv.save()
        invoice_id = recv.invoice_id

    return (address, invoice_id)


def payment_handler(request, invoice_id, secret):
    """Handle the response from blockchain.info."""
    address = request.GET.get('address')
    confirmations = request.GET.get('confirmations')
    tx_hash = request.GET.get('transaction_hash')
    value = int(request.GET.get('value'))
    order = get_object_or_404(BtcInvoice, invoice_id=invoice_id)

    if address != order.address:
        return HttpResponseBadRequest('Incorrect Receiving Address')
    if secret != settings.SECRET_KEY:
        return HttpResponseBadRequest('Invalid secret')
    if int(confirmations) >= 4:
        pay = BtcInvoicePayment(
            transaction_hash=tx_hash,
            value=value,
            invoice=order
        )
        pay.save()
        obj = get_object_or_404(BtcPendingInvoicePayment, invoice_id=invoice_id)
        obj.delete()
        return HttpResponse('*ok*', content_type='text/plain')
    else:
        pending, created = BtcPendingInvoicePayment.objects.get_or_create(
            invoice_id=invoice_id,
            transaction_hash=tx_hash,
            value=value,
        )
        return HttpResponse('Waiting for confirmations')
    # should never reach here!
    return HttpResponseServerError('Something went wrong')
