from django.conf.urls import url
from . import views

urlpatterns = [
    url(r"^options$", views.filter_by_options, name='filter_by_options'),
    url(r"^checkout$", views.checkout_steps, name="shop_checkout"),
    url(r"^product/(?P<slug>.*)$", views.product, name="shop_product"),
    url(r"^recently_viewed$", views.recent_products, name='recently_viewed')
]
