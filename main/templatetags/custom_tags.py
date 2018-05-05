from cartridge.shop.templatetags.shop_tags import _order_totals
from django.core.exceptions import ImproperlyConfigured
from django import template
from cartridge.shop.models import ProductOption
register = template.Library()


@register.filter
def by_type(objects, t):
    """
    Filter given list of objects by 'type' attribute.

    Used for filtering ProducOption objects.
    """
    return filter(lambda x: x.type == t, objects)


@register.simple_tag
def product_options():
    """Return all the available ProductOption objects."""
    opts = ProductOption.objects.all()
    return opts


@register.simple_tag(takes_context=True)
def get_total(context):
    """Return order total."""
    ot = _order_totals(context)
    total = ot.get('order_total')
    return total


@register.simple_tag
def load_siteconfig():
    """
    Add the 'SiteConfiguration' instance to the context.

    It also uses the request object as cache to avoid some DB hits.
    """
    from mezzanine.core.request import current_request
    try:
        from main.models import SiteConfiguration
    except ImportError:
        raise ImproperlyConfigured(
            "You must create a SiteConfiguration model"
            "to use load_siteconfig tag.")

    request = current_request()
    if hasattr(request, "siteconfig"):
        return request.siteconfig
    siteconfig = SiteConfiguration.objects.get_or_create()[0]
    request.siteconfig = siteconfig
    return siteconfig
