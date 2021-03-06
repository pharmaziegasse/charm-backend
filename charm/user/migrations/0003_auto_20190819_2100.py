# Generated by Django 2.2.3 on 2019-08-19 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190819_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='coach',
            field=models.CharField(blank=True, help_text="If registering a user, set the user's coach", max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_coach',
            field=models.BooleanField(default=False, help_text='Establish if the user is a coach'),
        ),
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, help_text='Address', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, help_text='City', max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, help_text='Country Code (e.g. AT)', max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_customer',
            field=models.BooleanField(default=True, help_text='Establish if the user is a customer'),
        ),
        migrations.AlterField(
            model_name='user',
            name='postal_code',
            field=models.CharField(blank=True, help_text='Postal Code', max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='registration_data',
            field=models.TextField(blank=True, help_text='JSON data', null=True),
        ),
    ]
