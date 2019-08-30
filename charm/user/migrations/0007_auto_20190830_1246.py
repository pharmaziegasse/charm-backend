# Generated by Django 2.2.3 on 2019-08-30 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20190829_1912'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'permissions': [('coach', 'The user is a coach')]},
        ),
        migrations.AlterField(
            model_name='user',
            name='title',
            field=models.CharField(blank=True, help_text='Title', max_length=20, null=True),
        ),
    ]
