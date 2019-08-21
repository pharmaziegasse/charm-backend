from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class _S_ParagraphBlock(blocks.StructBlock):
    statement = blocks.CharBlock(null=True, blank=True)
    paragraph = blocks.RichTextBlock(null=True, blank=False, features=[
        'bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link',
        'superscript', 'subscript', 'document-link', 'image', 'code'
        ], classname="full")

class _S_ArticleBlock(blocks.StructBlock):
    article_header = blocks.CharBlock(null=True, blank=True)
    paragraphs = blocks.StreamBlock([
        # Paragraph blocks are rendered in case a specific statement, which each paragraph has, is true
        ('s_paragraph', _S_ParagraphBlock(null=True, blank=False, icon='group', label="Paragraph"))
    ], null=True, blank=False)

class ReportsPage(Page):
    # paragraphs = StreamField([
    #     ('s_paragraph', _S_ParagraphBlock(null=True, blank=False, icon='group'))
    # ], null=True, blank=False)

    articles = StreamField([
        # Article blocks do contain headings and constit of multiple paragraphs
        ('s_article', _S_ArticleBlock(null=True, blank=False, icon='group', label="Article"))
    ], null=True, blank=False)

    # These panels will be listed on the Wagtail admin site where you can edit the page.
    main_content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('articles')
    ]

    # By defining the edit_handler, the panels are finally displayed
    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading='Main')
    ])