# Generated by Django 2.2.9 on 2019-12-27 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_webhooktransaction'),
    ]

    operations = [
        migrations.DeleteModel(
            name='WebhookTransaction',
        ),
    ]
