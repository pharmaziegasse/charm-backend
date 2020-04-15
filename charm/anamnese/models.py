import json
import os
import pytz

from charm.coach.models import Coach

from django.conf import settings
# This returns the currently active user model
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from django.utils import timezone

from .document import handle_excel

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

class AnamneseDocument(models.Model):
    link = models.CharField(
        null=True, blank=True,
        max_length=256
    )


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
    document = models.ForeignKey(
        AnamneseDocument,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='Document_AN'
    )
    form_data = models.TextField(
        null=True, blank=True
    )

    # custom save function
    def save(self, *args, **kwargs):
        today = timezone.now()

        # Set the creation date
        if not self.date:
            self.date = today

        # Save the anamnese in following format
        # Generating two anamnesis for the same person on the same day will intentially override the older one
        document_name = 'Anamnese_' \
            + self.user.first_name + '-' \
            + self.user.last_name + '_' \
            + today.strftime("%d-%m-%Y") \
            + '.xlsx'

        # In the settings file, the path for saving anamnesis excel documents is set with the AN_DOCUMENT_PATH variable
        # Get the document path, and, if the folder does not exist already, create it
        directory = settings.AN_DOCUMENT_PATH
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Get the document's path and save it accordingly
        path = directory + document_name

        # Create the MS Excel sheet
        handle_excel(self.form_data, path)

        # Create an object for storing the anamensis' link
        alinkcollection = AnamneseDocument(
            link=path
        )

        alinkcollection.save()

        # Create the relation between the anamnesis' data's object and the link to the anamnesis Excel sheet
        self.document = alinkcollection

        super(Anamnese, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = "date"


class AnFormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Anamnese field")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return AnamneseFormSubmission

    def create_an(self, user, coach, form_data):
        an = Anamnese(
            user = user,
            coach = coach,
            form_data = form_data
        )

        an.save()

        return an

    def add_user_dict(user, full_values):
        user_data = {}
        
        if user.customer_id:
            user_data['customer_id'] = {
                "helpText": "Kundennummer",
                "value": user.customer_id
            }
        if user.title:
            user_data['title'] = {
                "helpText": "Titel",
                "value": user.title
            }
        user_data['first_name'] = {
            "helpText": "Vorname",
            "value": user.first_name
        }
        user_data['last_name'] = {
            "helpText": "Nachname",
            "value": user.last_name
        }
        user_data['telephone'] = {
            "helpText": "Telefonnummer",
            "value": user.telephone
        }
        
        user_data['email'] = {
            "helpText": "E-Mail",
            "value": user.email
        }

        if user.coach:
            user_data['coach_first_name'] = {
                "helpText": "Vorname Coach",
                "value": user.coach.first_name
            }
            user_data['coach_last_name'] = {
                "helpText": "Nachname Coach",
                "value": user.coach.last_name
            }
            user_data['coach_telephone'] = {
                "helpText": "Telefonnummer Coach",
                "value": user.coach.telephone
            }
            user_data['coach_email'] = {
                "helpText": "E-Mail Coach",
                "value": user.coach.email
            }
            
        if user.birthdate:
            user_data['birthdate'] = {
                "helpText": "Geburtsdatum",
                "value": user.birthdate
            }
        if user.city:
            user_data['city'] = {
                "helpText": "Stadt",
                "value": user.city
            }
        if user.address:
            user_data['address'] = {
                "helpText": "Adresse",
                "value": user.address
            }
        if user.postal_code:
            user_data['postal_code'] = {
                "helpText": "Postleitzahl",
                "value": user.postal_code
            }
        if user.country:
            user_data['country'] = {
                "helpText": "Staat",
                "value": user.country
            }
        if user.newsletter:
            newsletter_status = "Ja"
        else:
            newsletter_status = "Nein"
        user_data['newsletter'] = {
            "helpText": "Newsletter",
            "value": newsletter_status
        }

        user_data.update(full_values)

        return full_values

    def process_form_submission(self, form):
        user = get_user_model().objects.get(id=form.cleaned_data['uid'])

        form.full_values = add_user_dict(user, form.full_values)

        an = self.create_an(
            user = user,
            coach = form.user,
            form_data = json.dumps(form.full_values, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            an = an,
        )


class FormField(AbstractFormField):
    page = ParentalKey('AnFormPage', on_delete=models.CASCADE, related_name='form_fields')


class AnamneseFormSubmission(AbstractFormSubmission):
    an = models.ForeignKey(Anamnese, on_delete=models.CASCADE)