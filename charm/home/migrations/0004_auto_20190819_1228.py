# Generated by Django 2.2.3 on 2019-08-19 10:28

from django.db import migrations
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20190809_1419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charmpage',
            name='body',
            field=wagtail.core.fields.RichTextField(blank=True, help_text="Site's body", null=True),
        ),
    ]