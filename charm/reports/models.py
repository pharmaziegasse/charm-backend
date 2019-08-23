from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.core.models import Page


class _S_ParagraphBlock(blocks.StructBlock):
    statement = blocks.CharBlock(null=True, blank=True, required=False)
    paragraph = blocks.RichTextBlock(null=True, blank=False, features=[
        'bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3',
        'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link',
        'superscript', 'subscript', 'document-link', 'image', 'code'
        ], classname="full")


class _S_SubChapterBlock(blocks.StructBlock):
    sub_chapter_header = blocks.CharBlock(null=True, blank=True)
    
    paragraphs = blocks.StreamBlock([
        # Paragraph blocks are rendered in case a specific statement, which each paragraph has, is true
        ('s_paragraph', _S_ParagraphBlock(null=True, blank=False, icon='group', label="Paragraph"))
    ], null=True, blank=False)

class _S_ChapterBlock(blocks.StructBlock):
    chapter_header = blocks.CharBlock(null=True, blank=True)

    sub_chapters = blocks.StreamBlock([
        ('s_subchapter', _S_SubChapterBlock(null=True, blank=False, icon='mail', label="Sub Chapter")),
        # Paragraph blocks are rendered in case a specific statement, which each paragraph has, is true
        ('s_paragraph', _S_ParagraphBlock(null=True, blank=False, icon='group', label="Paragraph"))
    ], null=True, blank=False)

class ReportsPage(Page):
    # paragraphs = StreamField([
    #     ('s_paragraph', _S_ParagraphBlock(null=True, blank=False, icon='group'))
    # ], null=True, blank=False)

    chapters = StreamField([
        # Article blocks do contain headings and constit of multiple paragraphs
        ('s_chapter', _S_ChapterBlock(null=True, blank=False, icon='group', label="Chapter"))
    ], null=True, blank=False)

    # These panels will be listed on the Wagtail admin site where you can edit the page.
    main_content_panels = [
        FieldPanel('title', classname="full title"),
        StreamFieldPanel('chapters')
    ]

    # By defining the edit_handler, the panels are finally displayed
    edit_handler = TabbedInterface([
        ObjectList(main_content_panels, heading='Main')
    ])