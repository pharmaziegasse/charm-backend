# Generated by Django 2.2.3 on 2019-08-29 09:48

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20190828_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_url',
            field=models.CharField(blank=True, help_text='Activation URL', max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='coach',
            field=models.ForeignKey(blank=True, help_text="Select the user's coach", null=True, on_delete=django.db.models.deletion.SET_NULL, to='coach.Coach'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='Establish if the user is a staff member.'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(blank=True, error_messages={'unique': 'A user with that username already exists.'}, help_text="Set this in case it's a staff account", max_length=36, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name="Username / Set this only if it's a staff account"),
        ),
    ]