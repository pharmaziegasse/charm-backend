# Generated by Django 2.2.3 on 2019-08-28 13:39

from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0004_auto_20190828_1415'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coach',
            fields=[
            ],
            options={
                'ordering': ('date_joined',),
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('user.user',),
        ),
    ]
