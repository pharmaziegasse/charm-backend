from django.db import models
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList, StreamFieldPanel, MultiFieldPanel

from .blocks import _H_HeroBlock, _S_AboutBlock, _S_ExpertsBlock, _S_FacebookBlock, _S_FeaturesBlock, _S_IndividualBlock, _S_InstagramBlock, _S_LabBlock, _S_ManifestBlock, _S_MethodBlock, _S_PricingBlock, _S_ReviewsBlock, _S_ServicesBlock, _S_StepsBlock, _S_WhyBlock

# Custom Homepage Model to provide global data later on
class CharmPage(Page):
    # These panels will be listed on the Wagtail admin site where you can edit the page.
    main_content_panels = [
        FieldPanel('title', classname="full title"),
    ]

    # By defining the edit_handler, the panels are finally displayed
    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading='Main')
    ])


## Unique Homepage ##
class UniquePage(Page):
    city = models.CharField(null=True, blank=False, max_length=255)
    zip_code = models.CharField(null=True, blank=False, max_length=255)
    address = models.CharField(null=True, blank=False, max_length=255)
    telephone = models.CharField(null=True, blank=False, max_length=255)
    telefax = models.CharField(null=True, blank=False, max_length=255)
    vat_number = models.CharField(null=True, blank=False, max_length=255)
    whatsapp_telephone = models.CharField(null=True, blank=True, max_length=255)
    whatsapp_contactline = models.CharField(null=True, blank=True, max_length=255)
    tax_id = models.CharField(null=True, blank=False, max_length=255)
    trade_register_number = models.CharField(null=True, blank=False, max_length=255)
    court_of_registry = models.CharField(null=True, blank=False, max_length=255)
    place_of_registry = models.CharField(null=True, blank=False, max_length=255)
    trade_register_number = models.CharField(null=True, blank=False, max_length=255)
    ownership = models.CharField(null=True, blank=False, max_length=255)
    email = models.CharField(null=True, blank=False, max_length=255)

    copyrightholder = models.CharField(null=True, blank=False, max_length=255)

    about = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])
    privacy = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])

    sociallinks = StreamField([
        ('link', blocks.URLBlock(help_text="Important! Format https://www.domain.tld/xyz"))
    ])

    array = []
    def sociallink_company(self):
        for link in self.sociallinks:
            self.array.append(str(link).split(".")[1])
        return self.array


    headers = StreamField([
        ('h_hero', _H_HeroBlock(null=True, blank=False, icon='image')),
        ('code', blocks.RawHTMLBlock(null=True, blank=True, classname="full", icon='code'))
    ], null=True, blank=False)

    sections = StreamField([
        ('s_why', _S_WhyBlock(null=True, blank=False, icon='group')),
        ('s_individual', _S_IndividualBlock(null=True, blank=False, icon='user', max_num=1)),
        ('s_experts', _S_ExpertsBlock(null=True, blank=False, icon='pick', max_num=1)),
        ('s_lab', _S_LabBlock(null=True, blank=False, icon='snippet')),
        ('s_method', _S_MethodBlock(null=True, blank=False, icon='site')),
        ('s_services', _S_ServicesBlock(null=True, blank=False, icon='openquote')),
        ('s_reviews', _S_ReviewsBlock(null=True, blank=False, icon='form')),
        ('s_features', _S_FeaturesBlock(null=True, blank=False, icon='fa-th')),
        ('s_steps', _S_StepsBlock(null=True, blank=False, icon='fa-list-ul')),
        ('s_manifest', _S_ManifestBlock(null=True, blank=False, icon='fa-comments')),
        ('s_facebook', _S_FacebookBlock(null=True, blank=False, icon='fa-facebook-official')),
        ('s_instagram', _S_InstagramBlock(null=True, blank=False, icon='fa-instagram')),
        ('s_pricing', _S_PricingBlock(null=True, blank=False, icon='home')),
        ('s_about', _S_AboutBlock(null=True, blank=False, icon='fa-quote-left')),
        ('code', blocks.RawHTMLBlock(null=True, blank=True, classname="full", icon='code'))
    ], null=True, blank=False)

    token = models.CharField(null=True, blank=True, max_length=255)

    main_content_panels = [
        StreamFieldPanel('headers'),
        StreamFieldPanel('sections')
    ]

    imprint_panels = [
        MultiFieldPanel(
            [
            FieldPanel('city'),
            FieldPanel('zip_code'),
            FieldPanel('address'),
            FieldPanel('telephone'),
            FieldPanel('telefax'),
            FieldPanel('whatsapp_telephone'),
            FieldPanel('whatsapp_contactline'),
            FieldPanel('email'),
            FieldPanel('copyrightholder')
            ],
            heading="contact",
        ),
        MultiFieldPanel(
            [
            FieldPanel('vat_number'),
            FieldPanel('tax_id'),
            FieldPanel('trade_register_number'),
            FieldPanel('court_of_registry'),
            FieldPanel('place_of_registry'),
            FieldPanel('trade_register_number'),
            FieldPanel('ownership')
            ],
            heading="legal",
        ),
        StreamFieldPanel('sociallinks'),
        MultiFieldPanel(
            [
            FieldPanel('about'),
            FieldPanel('privacy')
            ],
            heading="privacy",
        )
    ]

    token_panel = [
        FieldPanel('token')
    ]

    edit_handler = TabbedInterface([
        ObjectList(Page.content_panels + main_content_panels, heading='Main'),
        ObjectList(imprint_panels, heading='Imprint'),
        ObjectList(Page.promote_panels + token_panel + Page.settings_panels, heading='Settings', classname="settings")
    ])
