from django import forms
from cartridge.shop.forms import OrderForm
from mezzanine.conf import settings
from mezzanine.core.forms import Html5Mixin


class CustomOrderForm(Html5Mixin, OrderForm):
    """
    Subclass Html5Mixin for adding 'required' attribute to required fields.

    Subclass OrderForm to override country fields.
    Populate country list from settings.
    """

    def __init__(self, *args, **kwargs):
        """
        Change card fields required attribute to false.

        We don't need card fields because we use bitcoin for payments.
        """
        super(CustomOrderForm, self).__init__(*args, **kwargs)
        for field in self.card_fields:
            field.field.required = False

    billing_detail_country = forms.ChoiceField(choices=settings.COUNTRY_LIST)
    shipping_detail_country = forms.ChoiceField(choices=settings.COUNTRY_LIST)
