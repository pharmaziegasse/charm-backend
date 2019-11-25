import json

from charm.coach.models import Coach

# This returns the currently active user model
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from django.utils import timezone

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

class Q1FormField(AbstractFormField):
   page = ParentalKey('Q1FormPage', on_delete=models.CASCADE, related_name='form_fields')

class Q2FormField(AbstractFormField):
   page = ParentalKey('Q2FormPage', on_delete=models.CASCADE, related_name='form_fields')

class Q3FormField(AbstractFormField):
   page = ParentalKey('Q3FormPage', on_delete=models.CASCADE, related_name='form_fields')


class Questionnaire_1(models.Model):
    date = models.DateTimeField(
        null=True, blank=True
    )
    # This field identifies to which user the questionnaire belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )
    # To identify which coach created this questionnaire
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_Q'
    )
    # related_to = models.TextField(
    #     null=True, blank=False
    # )
    form_data = models.TextField(
        null=True, blank=True
    )

    class Meta:
        get_latest_by = "date"

class Q1FormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Questionnaire 1 fields")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return Q1FormSubmission

    def create_q1(self, date, user, coach, form_data):
        q1 = Questionnaire_1(
            date = date,
            user = user,
            coach = coach,
            form_data = form_data
        )

        q1.save()

        return q1

    def process_form_submission(self, form):
        user = get_user_model().objects.get(id=form.cleaned_data['uid'])

        q1 = self.create_q1(
            date = timezone.now(),
            user = user,
            coach = form.user,
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            q1 = q1,
        )

class Questionnaire_2(models.Model):
    date = models.DateTimeField(
        null=True, blank=True
    )
    # This field identifies to which user the questionnaire belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )
    # To identify which coach created this questionnaire
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_Q2'
    )
    # related_to = models.TextField(
    #     null=True, blank=False
    # )
    form_data = models.TextField(
        null=True, blank=True
    )

    class Meta:
        get_latest_by = "date"

class Q2FormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Questionnaire 2 fields")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return Q2FormSubmission

    def create_q2(self, date, user, coach, form_data):
        q2 = Questionnaire_2(
            date = date,
            user = user,
            coach = coach,
            form_data = form_data
        )

        q2.save()

        return q2

    def process_form_submission(self, form):
        user = get_user_model().objects.get(id=form.cleaned_data['uid'])

        q2 = self.create_q2(
            date = timezone.now(),
            user = user,
            coach = form.user,
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            q2 = q2,
        )

class Questionnaire_3(models.Model):
    date = models.DateTimeField(
        null=True, blank=True
    )
    # This field identifies to which user the questionnaire belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )
    # To identify which coach created this questionnaire
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_Q3'
    )
    # related_to = models.TextField(
    #     null=True, blank=False
    # )
    form_data = models.TextField(
        null=True, blank=True
    )

    class Meta:
        get_latest_by = "date"

class Q3FormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Questionnaire 3 fields")
            ],
            heading="Form Fields",
        )
    ]

    def is_valid(self):
        return True

    def get_submission_class(self):
        return Q3FormSubmission

    def create_q3(self, date, user, coach, form_data):
        q3 = Questionnaire_3(
            date = date,
            user = user,
            coach = coach,
            form_data = form_data
        )

        q3.save()

        return q3

    def process_form_submission(self, form):
        user = get_user_model().objects.get(id=form.cleaned_data['uid'])

        q3 = self.create_q3(
            date = timezone.now(),
            user = user,
            coach = form.user,
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            q3 = q3,
        )


class Q1FormSubmission(AbstractFormSubmission):
    q1 = models.ForeignKey(Questionnaire_1, on_delete=models.CASCADE)

class Q2FormSubmission(AbstractFormSubmission):
    q2 = models.ForeignKey(Questionnaire_2, on_delete=models.CASCADE)

class Q3FormSubmission(AbstractFormSubmission):
    q3 = models.ForeignKey(Questionnaire_3, on_delete=models.CASCADE)