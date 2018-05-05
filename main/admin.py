from django.contrib import admin
from mezzanine.pages.admin import PageAdmin
from mezzanine.galleries.models import Gallery
from mezzanine.galleries.admin import GalleryAdmin
from mezzanine.forms.models import Form
from mezzanine.forms.admin import FormAdmin
from mezzanine.core.admin import StackedDynamicInlineAdmin
from mezzanine.core.admin import TabularDynamicInlineAdmin
from mezzanine.utils.admin import SingletonAdmin
from mezzanine.blog.admin import BlogPostAdmin
from cartridge.shop.admin import ProductAdmin
from .models import IconBlurb, Homepage, FaqPage, FaqEntry, SiteConfiguration


class IconBlurbAdmin(StackedDynamicInlineAdmin):
    """Admin class for IconBlurb model."""

    model = IconBlurb


class HomepageAdmin(PageAdmin):
    """Admin class for Homepage model.

    Inline IconBlurbAdmin for adding/removing
    arbitrary number of Icon Blurbs
    """

    inlines = [IconBlurbAdmin, ]


class FaqEntryAdmin(TabularDynamicInlineAdmin):
    """Admin class for FaqEntry model."""

    model = FaqEntry


class FaqPageAdmin(PageAdmin):
    """Admin class for FaqPage model.

    Inlines FaqEntryAdmin for adding/removing
    arbitrary number of FAQ entries.
    """

    inlines = [FaqEntryAdmin, ]


class NoCSSGalleryAdmin(GalleryAdmin):
    """Remove css from GalleryAdmin."""

    class Media:
        extend = False


class CustomFormAdmin(FormAdmin):
    """Add IconBlurbs to FormAdmin.

    Used in Contact page for displaying
    address, email, etc blocks in contact page.
    """

    def __init__(self, *args, **kwargs):
        """Extend parent class inlines tuple."""
        super(CustomFormAdmin, self).__init__(*args, **kwargs)
        self.inlines += (IconBlurbAdmin, )

# Add custom fields to product admin and blogpost admin. Both fields
# are  defined in EXTRA_MODEL_FIELDS setting in settings.py file
ProductAdmin.fieldsets[0][1]["fields"].extend(["image_back"])
BlogPostAdmin.fieldsets[0][1]["fields"].insert(-2, "lead")

admin.site.register(SiteConfiguration, SingletonAdmin)
admin.site.register(Homepage, HomepageAdmin)
admin.site.register(FaqPage, FaqPageAdmin)
admin.site.unregister(Gallery)
admin.site.register(Gallery, NoCSSGalleryAdmin)
admin.site.unregister(Form)
admin.site.register(Form, CustomFormAdmin)
