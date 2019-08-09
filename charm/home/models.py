from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, TabbedInterface, ObjectList

# Custom Homepage Model to provide global data later on
class CharmPage(Page):
    body = RichTextField(null=True, blank=True, help_text="Site's body")
    
    # These panels will be listed on the Wagtail admin site where you can edit the page.
    main_content_panels = [
        FieldPanel('title', classname="full title"),
        FieldPanel('body', classname="full"),
    ]

    # By defining the edit_handler, the panels are finally displayed
    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading='Main')
    ])