from django.contrib.auth import get_user_model

from django.db import models

from charm.user.models import User

class Anamnese(models.Model):
    # This field identifies to which user the anamnese report belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
        )
    form_data = models.TextField(
        null=True, blank=True
    )