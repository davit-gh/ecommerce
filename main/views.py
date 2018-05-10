from collections import deque
from django.utils.translation import ugettext as _
from django.shortcuts import render
from cartridge.shop.models import Product
from cartridge.shop import views
from mezzanine.conf import settings
from .forms import CustomOrderForm


def checkout_steps(request):
    """
    Add shipping and tax info into to the request and sets new form_class.

    Added info is used for order total calculation on the first checkout step.
    Sets custom form_class inherited from OrderForm.
    """
    views.billship_handler(request, None)
    views.tax_handler(request, None)
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
        products = Product.objects.published().filter(
            categories__options__in=opt_ids
        ).distinct()
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
