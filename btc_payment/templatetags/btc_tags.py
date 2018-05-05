from blockchain.exchangerates import to_btc
from django import template
from ..views import create_handler
register = template.Library()


@register.simple_tag(takes_context=True)
def btc_context(context, total):
    """
    Receive context and order total.

    Return BTC address and BTC total
    """
    btc_total = to_btc('USD', total)
    request = context["request"]
    addr, inv_id = create_handler(request, total, btc_total)
    btc_context = {
        'btc_total': btc_total,
        'address': addr, 'invoice_id': inv_id
    }
    return btc_context
