from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList

class CharmPage(Page):
    body = RichTextField(blank=True, help_text="Site's body")

    main_content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]

    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading='Main')
    ])
