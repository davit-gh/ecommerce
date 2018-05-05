from django.conf.urls import url
from .views import payment_handler
from .views import create_handler

urlpatterns = [
    url(
        r"^payment/(?P<invoice_id>.*)/(?P<secret>.*)",
        payment_handler,
        name="payment_handler"
    ),
    url(
        r"^create/(?P<order_total>.*)/(?P<btc_total>.*)$",
        create_handler,
        name="create_handler"
    ),
]
