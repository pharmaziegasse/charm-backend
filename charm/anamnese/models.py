import json

from charm.coach.models import Coach

from datetime import datetime

# This returns the currently active user model
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

class FormField(AbstractFormField):
   page = ParentalKey('AnFormPage', on_delete=models.CASCADE, related_name='form_fields')

class Anamnese(models.Model):
    date = models.DateTimeField(
        null=True, blank=True
    )
    # This field identifies to which user the anamnese report belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )
    # To identify which coach created this anamnese
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_AN'
    )
    form_data = models.TextField(
        null=True, blank=True
    )

    class Meta:
        get_latest_by = "date"

class AnFormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Anamnese fields")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return AnamneseFormSubmission

    def create_an(self, date, user, coach, form_data):
        an = Anamnese(
            date = date,
            user = user,
            coach = coach,
            form_data = form_data
        )

        an.save()

        return an

    def process_form_submission(self, form):
        today = datetime.today()

        an = self.create_an(
            date = today.strftime("%Y-%m-%d %H:%M:%S"),
            user = get_user_model().objects.get(id=form.cleaned_data['uid']),
            coach = form.user,
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            an = an,
        )

class AnamneseFormSubmission(AbstractFormSubmission):
    an = models.ForeignKey(Anamnese, on_delete=models.CASCADE)