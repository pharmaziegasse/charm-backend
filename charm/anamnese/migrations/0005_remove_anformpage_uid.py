# Generated by Django 2.2.3 on 2019-08-21 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anamnese', '0004_auto_20190821_1208'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anformpage',
            name='uid',
        ),
    ]
