from django.conf.urls import url
from mezzanine.conf import settings
from . import views

_slash = "/" if settings.APPEND_SLASH else ""

urlpatterns = [
    url("^options%s$" % _slash, views.filter_by_options, name='filter_by_options'),
    url("^checkout%s$" % _slash, views.checkout_steps, name="shop_checkout"),
    url("^cart%s$" % _slash, views.cart, name="shop_cart"),
    url("^paypal_success%s$" % _slash, views.paypal_success, name="ppl"),
    url("^product/(?P<slug>.*)%s$" % _slash, views.product, name="shop_product"),
    url("^recently_viewed$", views.recent_products, name='recently_viewed')
]
