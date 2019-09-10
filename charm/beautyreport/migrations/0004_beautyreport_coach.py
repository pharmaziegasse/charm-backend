# Generated by Django 2.2.3 on 2019-09-10 22:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coach', '0001_initial'),
        ('beautyreport', '0003_auto_20190828_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='beautyreport',
            name='coach',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='BR_Coach', to='coach.Coach'),
        ),
    ]
