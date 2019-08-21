import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission


class FormField(AbstractFormField):
   page = ParentalKey('BrFormPage', on_delete=models.CASCADE, related_name='form_fields')

class Beautyreport(models.Model):
    date = models.DateTimeField(
        null=True, blank=True
    )
    # This field identifies to which user the anamnese report belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )
    form_data = models.TextField(
        null=True, blank=True
    )

    class Meta:
        get_latest_by = "date"

class BrFormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Beautyreport fields")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return BeautyreportFormSubmission

    def create_br(self, date, user, form_data):
        br = Beautyreport(
            date = date,
            user = user,
            form_data = form_data
        )

        br.save()

        return br

    def process_form_submission(self, form):
        today = datetime.today()

        br = self.create_br(
            date = today.strftime("%Y-%m-%d %H:%M:%S"),
            user = get_user_model().objects.get(id=form.cleaned_data['uid']),
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            br = br,
        )

class BeautyreportFormSubmission(AbstractFormSubmission):
    br = models.ForeignKey(Beautyreport, on_delete=models.CASCADE)