from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext, ugettext_lazy as _
from django.db import models
from mezzanine.pages.models import Page
from mezzanine.core.models import Orderable
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.core.models import SiteRelated
from cartridge.shop.models import Product

from datetime import datetime
from mezzanine.utils.timezone import get_best_local_timezone
from mezzanine.conf import settings
from pytz import timezone


@python_2_unicode_compatible
class SiteConfiguration(SiteRelated):
    """Singleton model for storing site-wide variables."""

    logo = FileField("Logo", upload_to="site", format="Image", blank=True)
    logo_small = FileField(
        _("Small Logo"), upload_to="site",
        format="Image", blank=True
    )
    favicon = FileField(
        _("Favicon"), upload_to="site", blank=True,
        help_text=_("An image that appears in the browser tab")
    )
    footer_address = RichTextField(
        default=_("Our address"),
        help_text=_("Company address displayed in footer."))
    footer_subscribe_info = models.CharField(
        max_length=200,
        default=_("Pellentesque habitant morbi tristique senectus et netus \
                et malesuada fames ac turpis egestas."),
        help_text=_("Text displayed above the subscription email field.")
    )

    def __str__(self):
        return str(self.site)

    class Meta:
        verbose_name = verbose_name_plural = _("Site Configuration")


class Homepage(Page):
    """Main class for homepage."""

    product_heading = models.CharField(
        max_length=100,
        default=_("Hot This Week"),
        help_text=_("A header displayed above the products.")
    )
    second_slider_heading = models.CharField(
        max_length=100,
        default=_("GET INSPIRED"),
        help_text=_("A header displayed above the 2nd slider.")
    )
    second_slider_subheading = models.CharField(
        max_length=100,
        default=_("Get the inspiration from our world class designers"),
        help_text=_("A subheader displayed above the 2nd slider.")
    )
    blog_heading = models.CharField(
        max_length=100,
        default=_("FROM OUR BLOG"),
        help_text=_("A header displayed above blog entries")
    )
    blog_subheading = models.CharField(
        max_length=100,
        default=_("What's new in the world of fashion?"),
        help_text=_("A subheader displayed above blog entries")
    )
    featured_products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name=_("Featured Products")
    )

    class Meta:
        verbose_name = _("Home page")
        verbose_name_plural = _("Home pages")


class IconBlurb(Orderable):
    """An icon block on a Page."""

    page = models.ForeignKey(Page, related_name="blurbs")
    icon_class = models.CharField(max_length=50)
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.CharField(
        max_length=200, blank=True,
        help_text=_("Optional, if provided clicking the blurb will go here.")
    )

    def __unicode__(self):
        return self.title


class FaqEntry(Orderable):
    """Model for FAQ entries."""

    title = models.CharField(max_length=100)
    content = models.TextField()
    page = models.ForeignKey("FaqPage", related_name="faqs", null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("FA question")
        verbose_name_plural = _("FA questions")


class FaqPage(Page):
    """New Page subclass to accommodate FAQ entries."""

    subheader = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = _("FAQ page")
        verbose_name_plural = _("FAQ pages")


class ProductExtend(object):
    """Extend Product class to add new function."""

    def is_new(self):
        """Check whether a product is new."""
        date_added_exists = True
        tz = timezone(get_best_local_timezone())
        try:
            time_delta = datetime.now(tz) - self.date_added
        except TypeError:
            date_added_exists = False
        isnew = date_added_exists and time_delta.days < settings.IS_NEW_DAYS
        return isnew

Product.__bases__ += (ProductExtend,)
