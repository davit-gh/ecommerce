from collections import deque
from django.utils.translation import ugettext as _
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.db import models
from cartridge.shop.templatetags.shop_tags import _order_totals
from cartridge.shop.models import Product, Category
from cartridge.shop.models import ProductVariation, DiscountCode
from cartridge.shop import views
from cartridge.shop.utils import clear_session
from mezzanine.conf import settings
from .forms import CustomOrderForm
import json


def get_paypal_params(request):
    """
    A function to construct JSON variable from the request object.

    The constructed object is then passed to Paypal Chechout button renderer.
    The variable is passed to the js function from the cart.html template.
    """
    items = []
    ot = _order_totals({'request': request})
    shipping = ot.get("shipping_total")
    tax = ot.get("tax_total")
    subtotal = float(request.cart.total_price())
    total = float(ot.get('order_total'))
    for item in request.cart:
        items.append({
            'name': item.description, 'quantity': item.quantity,
            'price': float(item.unit_price), 'sku': item.sku,
            'currency': 'USD'
        })
    transactions = [{
        'amount': {
            'total': total,
            'currency': 'USD',
            'details': {
                'subtotal': subtotal,
                'tax': tax,
                'shipping': shipping
            }
        },
        'item_list': {
            'items': items
        }
    }]
    data = {
        'transactions': transactions,
        'note_to_payer': 'Please contact us for any questions with the order.'
    }
    return json.dumps(data)


def paypal_success(request):
    """
    Copied over from cartridge.shop.models.Order.complete.

    Avoiding to copy the code would result in an unnecessary hassle
    of creating an Order object which is not required with Paypal.
    """
    session_fields = ("shipping_type", "shipping_total", "discount_total",
                      "discount_code", "tax_type", "tax_total")
    items = []
    if request.session.get('cart'):
        for item in request.cart.items.all():
            items.append({
                'image': item.image, 'title': item.description,
                'get_absolute_url': item.get_absolute_url()
            })
        discount_code = request.session.get('discount_code')
        clear_session(request, "order", *session_fields)
        for item in request.cart:
            try:
                variation = ProductVariation.objects.get(sku=item.sku)
            except ProductVariation.DoesNotExist:
                pass
            else:
                variation.update_stock(item.quantity * -1)
                variation.product.actions.purchased()
        if discount_code:
            DiscountCode.objects.active().filter(code=discount_code).update(
                uses_remaining=models.F('uses_remaining') - 1)
        request.cart.delete()
        del request.session['cart']
    else:
        raise PermissionDenied
    return render(request, "shop/paypal_complete.html", {'items': items})


def cart(request):
    """
    Override cartridge.shop.views.cart function to add extra context.

    Add shipping and tax info into to the request.
    The extra_context variable contains the json-encoded payment data.
    """
    views.billship_handler(request, None)
    views.tax_handler(request, None)
    ppl_data = get_paypal_params(request)
    extra_context = {'paypal_data': ppl_data}
    return views.cart(request, extra_context=extra_context)


def checkout_steps(request):
    """
    Set a custom form_class.

    Sets custom form_class inherited from OrderForm.
    """
    return views.checkout_steps(request, form_class=CustomOrderForm)


def _render_products(request, products, header):
    """
    Utility function for rendering a group of products.

    Sets context variables and calls render().
    """
    context = {
        'products': products,
        'header': header
    }
    return render(request, 'shop/products.html', context)


def filter_by_options(request):
    """
    Retrieve products containing options selected by the user.

    Called when options are applied on left sidebar of product/category pages.
    """
    if request.method == 'POST':
        opt_ids = request.POST.getlist('checkboxes')
        categories = Category.objects.filter(options__in=opt_ids)
        products = []
        for category in categories:
            products += category.products.filter(category.filters()).distinct()
        # products = Product.objects.published().filter(
        #     categories__options__in=opt_ids
        # ).distinct()
        header = _("Filtered Products")
        return _render_products(request, products, header)


def recent_products(request):
    """
    Retrieve recently viewed products from the context.

    Calls _render_products for rendering.
    """
    if request.method == 'GET':
        slugs = request.session.get("recent_slugs", [])
        products = Product.objects.published().filter(slug__in=slugs)
        header = _("Products viewed recently")
        return _render_products(request, products, header)


def _add2session(request, slug):
    """
    Use deque with configurable maxlen for storing slugs in session.

    Stored slugs are then used to retrieve recently viewed products.
    Convert deque to list before storing in session because
    session variables need to be json serializable.
    """
    maxlen = settings.RECENT_MAXLEN
    recent_slugs = request.session.get("recent_slugs", [])
    recent_slugs = deque(set(recent_slugs), maxlen=maxlen)
    recent_slugs.append(slug)
    request.session['recent_slugs'] = list(recent_slugs)
    return request


def product(request, slug):
    """
    Add recently viewed products to extra_context of shop.views.product.

    Retrieve those products from slugs in session and pass them along
    to be rendered on product page.
    """
    new_request = _add2session(request, slug)
    slugs = new_request.session.get("recent_slugs", [])
    products = Product.objects.published().filter(slug__in=slugs)
    extra = {'recent_products': products}
    return views.product(new_request, slug, extra_context=extra)
