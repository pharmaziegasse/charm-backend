# Generated by Django 2.2.3 on 2019-08-21 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anamnese', '0003_anformpage_user_panel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='anformpage',
            name='user_panel',
        ),
        migrations.AddField(
            model_name='anformpage',
            name='uid',
            field=models.IntegerField(null=True),
        ),
    ]