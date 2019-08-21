# Generated by Django 2.2.3 on 2019-08-21 15:45

from django.db import migrations
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_reportspage_paragraphs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reportspage',
            name='paragraphs',
        ),
        migrations.AddField(
            model_name='reportspage',
            name='articles',
            field=wagtail.core.fields.StreamField([('s_article', wagtail.core.blocks.StructBlock([('article_header', wagtail.core.blocks.CharBlock(blank=True, null=True)), ('paragraphs', wagtail.core.blocks.StreamBlock([('s_paragraph', wagtail.core.blocks.StructBlock([('statement', wagtail.core.blocks.CharBlock(blank=True, null=True)), ('paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], null=True))], blank=False, icon='group', label='Paragraph', null=True))], blank=False, null=True))], blank=False, icon='group', label='Article', null=True))], null=True),
        ),
    ]
