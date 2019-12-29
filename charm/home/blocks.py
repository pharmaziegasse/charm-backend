from django.db import models
from django.http import HttpResponse

from modelcluster.fields import ParentalKey

from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.admin.edit_handlers import PageChooserPanel, TabbedInterface, ObjectList, InlinePanel, StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField


from ..colorfield.fields import ColorField, ColorAlphaField
from ..colorfield.blocks import ColorBlock, ColorAlphaBlock, GradientColorBlock

from .snippets import Button

## Header ##
class Hero_SlideBlock(blocks.StructBlock):
    slide_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="The bold header text at the frontpage slider")
    slide_subhead = blocks.RichTextBlock(null=True, blank=False, help_text="The content of the frontpage slider element", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    slide_image = ImageChooserBlock(null=True, blank=False, help_text="Big, high resolution slider image")
    slide_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="The button displayed at the frontpage slider")

class  _H_HeroBlock(blocks.ListBlock):
    def __init__(self, **kwargs):
        super(_H_HeroBlock, self).__init__(Hero_SlideBlock(), **kwargs)


## Why Section ##
class Why_CollumBlock(blocks.StructBlock):
    collum_image = ImageChooserBlock(null=True, blank=False, help_text="Icon representating the below content")
    collum_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Formatted text", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

class _S_WhyBlock(blocks.StructBlock):
    why_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    why_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    why_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    why_collum1 = Why_CollumBlock(null=True, blank=False, icon='cogs', help_text="Left block")
    why_collum2 = Why_CollumBlock(null=True, blank=False, icon='cogs', help_text="Middle block")
    why_collum3 = Why_CollumBlock(null=True, blank=False, icon='cogs', help_text="Right block")
    why_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at why-section")


## Individual Section ##
class _S_IndividualBlock(blocks.StructBlock):
    individual_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    individual_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    individual_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    individual_image = ImageChooserBlock(null=True, blank=False, help_text="Individual-fitting image")
    individual_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Content paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    individual_footer = blocks.CharBlock(null=True, blank=True, required=False, classname="full title", help_text="Footer text")
    individual_footer_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    individual_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at individual-section")


## Experts Section ##
class _S_ExpertsBlock(blocks.StructBlock):
    experts_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    experts_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    experts_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    experts_image = ImageChooserBlock(null=True, blank=False, help_text="Experts-fitting image")
    experts_lead = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    experts_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Content paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    experts_footer = blocks.CharBlock(null=True, blank=True, required=False, classname="full title", help_text="Footer text")
    experts_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at expert-section")


## Lab Section ##
class _S_LabBlock(blocks.StructBlock):
    lab_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    lab_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    lab_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    lab_image = ImageChooserBlock(null=True, blank=False, help_text="Lab-fitting image")
    lab_lead = blocks.RichTextBlock(null=True, blank=False, help_text="Bigger leading RichText paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    lab_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Content paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    lab_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at lab-section")


## Method Section ##
class Method_SphereBlock(blocks.StructBlock):
    sphere_step = blocks.RichTextBlock(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

class _S_MethodBlock(blocks.StructBlock):
    method_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    method_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    method_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    method_sphere1 = Method_SphereBlock(null=True, blank=False, icon='cogs', help_text="Top sphere")
    method_sphere2 = Method_SphereBlock(null=True, blank=False, icon='cogs', help_text="Left sphere")
    method_sphere3 = Method_SphereBlock(null=True, blank=False, icon='cogs', help_text="Right sphere")
    method_sphere4 = Method_SphereBlock(null=True, blank=False, icon='cogs', help_text="Bottom sphere")
    method_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at method-section")


## Services Section ##
class Services_ServiceBlock(blocks.StructBlock):
    service_head = blocks.CharBlock(null=True, blank=False, help_text="Bold service header text")
    service_content = blocks.RichTextBlock(null=True, blank=False, help_text="Description of the service", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

class _S_ServicesBlock(blocks.StructBlock):
    services_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    services_services = blocks.StreamBlock([
        ('service', Services_ServiceBlock(null=True, blank=False, icon='doc-full'))
    ], null=True, blank=False)
    services_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at services-block")


## Reviews Section ##
class Reviews_ReviewBlock(blocks.StructBlock):
    review_image = ImageChooserBlock(null=True, blank=False, help_text="Picture of reviewing person")
    review_quote = blocks.RichTextBlock(null=True, blank=False, help_text="Customer's opinion", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    review_name = blocks.CharBlock(null=True, blank=False, classname="full", help_text="Reviewer's name")
    review_info = blocks.CharBlock(null=True, blank=False, classname="full", help_text="Additional reviewers information. E.g. profession")

class _S_ReviewsBlock(blocks.StructBlock):
    reviews_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    reviews_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    reviews_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    reviews_reviews = blocks.StreamBlock([
        ('review', Reviews_ReviewBlock(null=True, blank=False))
    ], null=True, blank=False)


## Features Section ##
class Features_FeatureBlock(blocks.StructBlock):
    feature_icon = blocks.CharBlock(null=True, blank=False, help_text="Font Awesome icon name (e.g. facebook-f) from https://fontawesome.com/icons?d=gallery&s=solid&m=free")
    feature_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    feature_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Feature paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

class _S_FeaturesBlock(blocks.StructBlock):
    features_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    features_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    features_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    features_subhead = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Smaller subhead text")
    features_displaysubhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    features_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at features-block")
    features_features = blocks.StreamBlock([
        ('feature', Features_FeatureBlock(null=True, blank=False))
    ], null=True, blank=False)


## Steps Section ##
class Steps_StepBlock(blocks.StructBlock):
    step_icon = blocks.CharBlock(null=True, blank=False, help_text="Font Awesome icon name (e.g. facebook-f) from https://fontawesome.com/icons?d=gallery&s=solid&m=free")
    step_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    step_image = ImageChooserBlock(null=True, blank=False, help_text="Image fitting this step")
    step_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Step paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

class _S_StepsBlock(blocks.StructBlock):
    steps_use_simple_design = blocks.BooleanBlock(null=True, blank=True, required=False, help_text="Use simple design without images")
    steps_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    steps_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    steps_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    steps_subhead = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Smaller subhead text")
    steps_displaysubhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    steps_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at steps-block")
    steps_steps = blocks.StreamBlock([
        ('step', Steps_StepBlock(null=True, blank=False))
    ], null=True, blank=False, max_num=4)


## Manifest Section ##
class _S_ManifestBlock(blocks.StructBlock):
    manifest_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    manifest_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    manifest_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Manifest paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    manifest_image = ImageChooserBlock(null=True, blank=False, help_text="Image fitting manifest-section")

# ## Specials Section ##
# class Specials_SpecialBlock(blocks.StructBlock):
#     special_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
#     special_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Special paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

# class _S_SpecialsBlock(blocks.StructBlock):
#     specials_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
#     specials_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
#     specials_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
#     specials_footer = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Footer text")
#     specials_image = ImageChooserBlock(null=True, blank=False, help_text="Image fitting specials-section")
#     specials_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at specials-block")
#     specials_specials = blocks.StreamBlock([
#       ('specials', Specials_SpecialBlock(null=True, blank=False))
#     ], null=True, blank=False, max_num=4)


# ## Coachings Section ##
# class Coachings_CoachingBlock(blocks.StructBlock):
#     coaching_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
#     coaching_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Coaching paragraph", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")

# class _S_CoachingsBlock(blocks.StructBlock):
#     coachings_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
#     coachings_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
#     coachings_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
#     coachings_footer = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Footer text")
#     coachings_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at coachings-block")
#     coachings_coachings = blocks.StreamBlock([
#       ('coachings', Specials_SpecialBlock(null=True, blank=False))
#     ], null=True, blank=False, max_num=4)


## Facebook Section ##
class Facebook_PostBlock(blocks.StructBlock):
    facebook_url = blocks.URLBlock(null=True, blank=False, classname="full", help_text="URL of Facebook-Post")

class _S_FacebookBlock(blocks.StructBlock):
    facebook_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    facebook_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    facebook_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    facebook_urls = blocks.StreamBlock([
        ('facebook', Facebook_PostBlock(null=True, blank=False))
    ], null=True, blank=False, max_num=3)


## Instagram Section ##
class Instagram_PostBlock(blocks.StructBlock):
    instagram_url = blocks.URLBlock(null=True, blank=False, classname="full", help_text="URL to Instagram-Post")

class _S_InstagramBlock(blocks.StructBlock):
    instagram_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    instagram_head = blocks.CharBlock(null=True, blank=False, classname="full title")
    instagram_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    instagram_captions = blocks.BooleanBlock(null=True, blank=True, required=False, help_text="Activate to show texts and hashtags of the given Instagram post on the website.")
    instagram_urls = blocks.StreamBlock([
        ('instagram',Instagram_PostBlock(null=True, blank=False))
    ], null=True, blank=False, max_num=3)


## Pricing Section ##
class Pricing_PricingcardBlock(blocks.StructBlock):
    pricingcard_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    pricingcard_title = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Title of pricing card")
    pricingcard_description = blocks.RichTextBlock(null=True, blank=False, help_text="Description of offer", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    pricingcard_price = blocks.DecimalBlock(null=True, blank=False, decimal_places=2, help="Price of the offer")
    pricingcard_sucessmsg = blocks.RichTextBlock(null=True, blank=False, help_text="Success message", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")
    pricingcard_button = SnippetChooserBlock(Button, null=True, blank=True, required=False, help_text="Button displayed at the pricing-section")

class _S_PricingBlock(blocks.StructBlock):
    pricing_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    pricing_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    pricing_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    pricing_pricingcards = blocks.StreamBlock([
        ('pricingcard', Pricing_PricingcardBlock(null=True, blank=False))
    ], null=True, blank=False, max_num=3)


## About Section ##
class _S_AboutBlock(blocks.StructBlock):
    about_background = ColorBlock(null=True, blank=False, help_text="Select background color that contrasts text")
    about_image = ImageChooserBlock(null=True, blank=False, help_text="Office-fitting image")
    about_displayhead = blocks.BooleanBlock(null=True, blank=True, default=True, required=False, help_text="Whether or not to display the header")
    about_head = blocks.CharBlock(null=True, blank=False, classname="full title", help_text="Bold header text")
    about_paragraph = blocks.RichTextBlock(null=True, blank=False, help_text="Paragraph about the company", features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], classname="full")