# Generated by Django 2.2.9 on 2019-12-28 19:57

import charm.colorfield.blocks
import charm.home.blocks
import charm.home.snippets
from django.db import migrations, models
import django.db.models.deletion
import wagtail.core.blocks
import wagtail.core.fields
import wagtail.images.blocks
import wagtail.snippets.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0041_group_collection_permissions_verbose_name_plural'),
        ('home', '0005_remove_charmpage_body'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniquePage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('city', models.CharField(max_length=255, null=True)),
                ('zip_code', models.CharField(max_length=255, null=True)),
                ('address', models.CharField(max_length=255, null=True)),
                ('telephone', models.CharField(max_length=255, null=True)),
                ('telefax', models.CharField(max_length=255, null=True)),
                ('vat_number', models.CharField(max_length=255, null=True)),
                ('whatsapp_telephone', models.CharField(blank=True, max_length=255, null=True)),
                ('whatsapp_contactline', models.CharField(blank=True, max_length=255, null=True)),
                ('tax_id', models.CharField(max_length=255, null=True)),
                ('court_of_registry', models.CharField(max_length=255, null=True)),
                ('place_of_registry', models.CharField(max_length=255, null=True)),
                ('trade_register_number', models.CharField(max_length=255, null=True)),
                ('ownership', models.CharField(max_length=255, null=True)),
                ('email', models.CharField(max_length=255, null=True)),
                ('copyrightholder', models.CharField(max_length=255, null=True)),
                ('about', wagtail.core.fields.RichTextField(null=True)),
                ('privacy', wagtail.core.fields.RichTextField(null=True)),
                ('sociallinks', wagtail.core.fields.StreamField([('link', wagtail.core.blocks.URLBlock(help_text='Important! Format https://www.domain.tld/xyz'))])),
                ('headers', wagtail.core.fields.StreamField([('h_hero', charm.home.blocks._H_HeroBlock(blank=False, icon='image', null=True)), ('code', wagtail.core.blocks.RawHTMLBlock(blank=True, classname='full', icon='code', null=True))], null=True)),
                ('sections', wagtail.core.fields.StreamField([('s_why', wagtail.core.blocks.StructBlock([('why_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('why_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('why_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('why_collum1', wagtail.core.blocks.StructBlock([('collum_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Icon representating the below content', null=True)), ('collum_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Formatted text', null=True))], blank=False, help_text='Left block', icon='cogs', null=True)), ('why_collum2', wagtail.core.blocks.StructBlock([('collum_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Icon representating the below content', null=True)), ('collum_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Formatted text', null=True))], blank=False, help_text='Middle block', icon='cogs', null=True)), ('why_collum3', wagtail.core.blocks.StructBlock([('collum_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Icon representating the below content', null=True)), ('collum_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Formatted text', null=True))], blank=False, help_text='Right block', icon='cogs', null=True)), ('why_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at why-section', null=True, required=False))], blank=False, icon='group', null=True)), ('s_individual', wagtail.core.blocks.StructBlock([('individual_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('individual_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('individual_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('individual_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Individual-fitting image', null=True)), ('individual_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Content paragraph', null=True)), ('individual_footer', wagtail.core.blocks.CharBlock(blank=True, classname='full title', help_text='Footer text', null=True, required=False)), ('individual_footer_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('individual_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at individual-section', null=True, required=False))], blank=False, icon='user', max_num=1, null=True)), ('s_experts', wagtail.core.blocks.StructBlock([('experts_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('experts_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('experts_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('experts_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Experts-fitting image', null=True)), ('experts_lead', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('experts_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Content paragraph', null=True)), ('experts_footer', wagtail.core.blocks.CharBlock(blank=True, classname='full title', help_text='Footer text', null=True, required=False)), ('experts_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at expert-section', null=True, required=False))], blank=False, icon='pick', max_num=1, null=True)), ('s_lab', wagtail.core.blocks.StructBlock([('lab_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('lab_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('lab_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('lab_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Lab-fitting image', null=True)), ('lab_lead', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Bigger leading RichText paragraph', null=True)), ('lab_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Content paragraph', null=True)), ('lab_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at lab-section', null=True, required=False))], blank=False, icon='snippet', null=True)), ('s_method', wagtail.core.blocks.StructBlock([('method_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('method_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('method_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('method_sphere1', wagtail.core.blocks.StructBlock([('sphere_step', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], null=True))], blank=False, help_text='Top sphere', icon='cogs', null=True)), ('method_sphere2', wagtail.core.blocks.StructBlock([('sphere_step', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], null=True))], blank=False, help_text='Left sphere', icon='cogs', null=True)), ('method_sphere3', wagtail.core.blocks.StructBlock([('sphere_step', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], null=True))], blank=False, help_text='Right sphere', icon='cogs', null=True)), ('method_sphere4', wagtail.core.blocks.StructBlock([('sphere_step', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], null=True))], blank=False, help_text='Bottom sphere', icon='cogs', null=True)), ('method_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at method-section', null=True, required=False))], blank=False, icon='site', null=True)), ('s_services', wagtail.core.blocks.StructBlock([('services_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('services_services', wagtail.core.blocks.StreamBlock([('service', wagtail.core.blocks.StructBlock([('service_head', wagtail.core.blocks.CharBlock(blank=False, help_text='Bold service header text', null=True)), ('service_content', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Description of the service', null=True))], blank=False, icon='doc-full', null=True))], blank=False, null=True)), ('services_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at services-block', null=True, required=False))], blank=False, icon='openquote', null=True)), ('s_reviews', wagtail.core.blocks.StructBlock([('reviews_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('reviews_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('reviews_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('reviews_reviews', wagtail.core.blocks.StreamBlock([('review', wagtail.core.blocks.StructBlock([('review_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Picture of reviewing person', null=True)), ('review_quote', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text="Customer's opinion", null=True)), ('review_name', wagtail.core.blocks.CharBlock(blank=False, classname='full', help_text="Reviewer's name", null=True)), ('review_info', wagtail.core.blocks.CharBlock(blank=False, classname='full', help_text='Additional reviewers information. E.g. profession', null=True))], blank=False, null=True))], blank=False, null=True))], blank=False, icon='form', null=True)), ('s_features', wagtail.core.blocks.StructBlock([('features_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('features_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('features_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('features_subhead', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Smaller subhead text', null=True)), ('features_displaysubhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('features_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at features-block', null=True, required=False)), ('features_features', wagtail.core.blocks.StreamBlock([('feature', wagtail.core.blocks.StructBlock([('feature_icon', wagtail.core.blocks.CharBlock(blank=False, help_text='Font Awesome icon name (e.g. facebook-f) from https://fontawesome.com/icons?d=gallery&s=solid&m=free', null=True)), ('feature_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('feature_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Feature paragraph', null=True))], blank=False, null=True))], blank=False, null=True))], blank=False, icon='fa-th', null=True)), ('s_steps', wagtail.core.blocks.StructBlock([('steps_use_simple_design', wagtail.core.blocks.BooleanBlock(blank=True, help_text='Use simple design without images', null=True, required=False)), ('steps_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('steps_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('steps_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('steps_subhead', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Smaller subhead text', null=True)), ('steps_displaysubhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('steps_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at steps-block', null=True, required=False)), ('steps_steps', wagtail.core.blocks.StreamBlock([('step', wagtail.core.blocks.StructBlock([('step_icon', wagtail.core.blocks.CharBlock(blank=False, help_text='Font Awesome icon name (e.g. facebook-f) from https://fontawesome.com/icons?d=gallery&s=solid&m=free', null=True)), ('step_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('step_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Image fitting this step', null=True)), ('step_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Step paragraph', null=True))], blank=False, null=True))], blank=False, max_num=4, null=True))], blank=False, icon='fa-list-ul', null=True)), ('s_manifest', wagtail.core.blocks.StructBlock([('manifest_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('manifest_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('manifest_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Manifest paragraph', null=True)), ('manifest_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Image fitting manifest-section', null=True))], blank=False, icon='fa-comments', null=True)), ('s_facebook', wagtail.core.blocks.StructBlock([('facebook_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('facebook_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('facebook_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('facebook_urls', wagtail.core.blocks.StreamBlock([('facebook', wagtail.core.blocks.StructBlock([('facebook_url', wagtail.core.blocks.URLBlock(blank=False, classname='full', help_text='URL of Facebook-Post', null=True))], blank=False, null=True))], blank=False, max_num=3, null=True))], blank=False, icon='fa-facebook-official', null=True)), ('s_instagram', wagtail.core.blocks.StructBlock([('instagram_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('instagram_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', null=True)), ('instagram_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('instagram_captions', wagtail.core.blocks.BooleanBlock(blank=True, help_text='Activate to show texts and hashtags of the given Instagram post on the website.', null=True, required=False)), ('instagram_urls', wagtail.core.blocks.StreamBlock([('instagram', wagtail.core.blocks.StructBlock([('instagram_url', wagtail.core.blocks.URLBlock(blank=False, classname='full', help_text='URL to Instagram-Post', null=True))], blank=False, null=True))], blank=False, max_num=3, null=True))], blank=False, icon='fa-instagram', null=True)), ('s_pricing', wagtail.core.blocks.StructBlock([('pricing_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('pricing_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('pricing_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('pricing_pricingcards', wagtail.core.blocks.StreamBlock([('pricingcard', wagtail.core.blocks.StructBlock([('pricingcard_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('pricingcard_title', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Title of pricing card', null=True)), ('pricingcard_description', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Description of offer', null=True)), ('pricingcard_price', wagtail.core.blocks.DecimalBlock(blank=False, decimal_places=2, help='Price of the offer', null=True)), ('pricingcard_sucessmsg', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Success message', null=True)), ('pricingcard_button', wagtail.snippets.blocks.SnippetChooserBlock(charm.home.snippets.Button, blank=True, help_text='Button displayed at the pricing-section', null=True, required=False))], blank=False, null=True))], blank=False, max_num=3, null=True))], blank=False, icon='home', null=True)), ('s_about', wagtail.core.blocks.StructBlock([('about_background', charm.colorfield.blocks.ColorBlock(blank=False, help_text='Select background color that contrasts text', null=True)), ('about_image', wagtail.images.blocks.ImageChooserBlock(blank=False, help_text='Office-fitting image', null=True)), ('about_displayhead', wagtail.core.blocks.BooleanBlock(blank=True, default=True, help_text='Whether or not to display the header', null=True, required=False)), ('about_head', wagtail.core.blocks.CharBlock(blank=False, classname='full title', help_text='Bold header text', null=True)), ('about_paragraph', wagtail.core.blocks.RichTextBlock(blank=False, classname='full', features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'], help_text='Paragraph about the company', null=True))], blank=False, icon='fa-quote-left', null=True)), ('code', wagtail.core.blocks.RawHTMLBlock(blank=True, classname='full', icon='code', null=True))], null=True)),
                ('token', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
        migrations.CreateModel(
            name='Button',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('button_title', models.CharField(max_length=255, null=True)),
                ('button_embed', models.CharField(blank=True, max_length=255, null=True)),
                ('button_link', models.URLField(blank=True, null=True)),
                ('button_page', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtailcore.Page')),
            ],
        ),
    ]
