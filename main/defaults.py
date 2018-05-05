from django.utils.translation import ugettext_lazy as _
from mezzanine.conf import register_setting

# newly registered social links
register_setting(
    name="SOCIAL_LINK_FACEBOOK",
    label=_("Facebook link"),
    description=_(
        "If present a Facebook icon linking here will be in the footer."),
    editable=True,
    default="https://www.facebook.com/<your-username>",
)

register_setting(
    name="SOCIAL_LINK_TWITTER",
    label=_("Twitter link"),
    description=_(
        "If present a Twitter icon linking here will be in the footer."),
    editable=True,
    default="https://twitter.com/<your-username>",
)

register_setting(
    name="SOCIAL_LINK_GOOGLE_PLUS",
    label=_("Google+ link"),
    description=_(
        "If present a Google+ icon linking here will be in the footer."),
    editable=True,
    default='http://plus.google.com/<your-username>/',
)

register_setting(
    name="SOCIAL_LINK_INSTAGRAM",
    label=_("Instagram link"),
    description=_(
        "If present a Instagram icon linking here will be in the footer."),
    editable=True,
    default='http://instagram.com/<your-username>/',
)

register_setting(
    name="EMAIL_LINK",
    label=_("Email link"),
    description=_(
        "If present a Email icon linking here will be in the footer."),
    editable=True,
    default='mailto:',
)

# appending new defined setting to TEMPLATE_ACCESSIBLE_SETTINGS
register_setting(
    name="TEMPLATE_ACCESSIBLE_SETTINGS",
    description=_("Sequence of setting names available within templates."),
    editable=False,
    default=(
        "SOCIAL_LINK_FACEBOOK",
        "SOCIAL_LINK_TWITTER",
        "SOCIAL_LINK_GOOGLE_PLUS",
        "SOCIAL_LINK_INSTAGRAM",
        "EMAIL_LINK"
    ),
    append=True,
)
