# Generated by Django 2.2.3 on 2019-09-10 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('anamnese', '0008_anamnese_coach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anamnese',
            name='coach',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='Coach_AN', to='coach.Coach'),
        ),
    ]
