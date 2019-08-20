from django.db import models

class Beautyreport(models.Model):
    uid = models.CharField(
        null=True, blank=False, max_length=36
    )