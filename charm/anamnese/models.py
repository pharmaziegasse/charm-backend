import json
import pytz

from charm.coach.models import Coach

# This returns the currently active user model
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from django.utils import timezone

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
        user = get_user_model().objects.get(id=form.cleaned_data['uid'])
     
        user_data = {}

        user_data['first_name'] = user.first_name
        user_data['last_name'] = user.last_name
        user_data['telephone'] = user.telephone
        user_data['email'] = user.email
        if user.coach:
            user_data['coach_first_name'] = user.coach.first_name
            user_data['coach_last_name'] = user.coach.last_name
            user_data['coach_telephone'] = user.coach.telephone
            user_data['coach_email'] = user.coach.email
            if user.coach.title:
                user_data['coach_title'] = user.coach.title
            if user.coach.birthdate:
                user_data['coach_birthdate'] = user.coach.birthdate
            if user.coach.address:
                user_data['coach_address'] = user.coach.address
            if user.coach.city:
                user_data['coach_city'] = user.coach.city
            if user.coach.postal_code:
                user_data['coach_postal_code'] = user.coach.postal_code
            if user.coach.country:
                user_data['coach_country'] = user.coach.country
        if user.title:
            user_data['title'] = user.title
        if user.birthdate:
            user_data['birthdate'] = user.birthdate
        if user.address:
            user_data['address'] = user.address
        if user.city:
            user_data['city'] = user.city
        if user.postal_code:
            user_data['postal_code'] = user.postal_code
        if user.country:
            user_data['country'] = user.country
        user_data['newsletter'] = user.newsletter

        form.cleaned_data.update(user_data)

        today = timezone.now()

        an = self.create_an(
            date = today.strftime("%Y-%m-%d %H:%M:%S"),
            user = user,
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