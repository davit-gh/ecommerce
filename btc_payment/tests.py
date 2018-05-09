from django.test.client import RequestFactory
from django.test import TestCase
from .models import BtcInvoice
from .views import create_handler


class BtcPaymentTests(TestCase):
    """BTC payment views testing class."""

    def setUp(self):
        """Test initialization."""
        self.factory = RequestFactory()

    def _create_handler(self, address, inv_id):
        invoice = BtcInvoice.objects.latest()
        # Set an address that has not received funds.
        invoice.address = address
        invoice.invoice_id = inv_id
        invoice.save()
        kwargs = {'order_total': 9.99, 'btc_total': 0.0000021}
        request = self.factory.get('/customer/details')
        request.COOKIES['sessionid'] = 'ddd'
        response = create_handler(request, **kwargs)
        return response

    # def _create_payment():
        # For the time of coding blockchain.info Receive V2 API
        # doesn't support test payments. No automatic test for payments now.

    def test_views(self):
        """Test create_handler() function with 'unused' BTC address."""
        response = self._create_handler(
            '129FNZEnkqweTtGfWSkuRkQrPk1k6FLo96', '1111'
        )
        self.assertEqual(
            response, ('129FNZEnkqweTtGfWSkuRkQrPk1k6FLo96', '1111')
        )
