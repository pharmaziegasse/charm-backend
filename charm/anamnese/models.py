import json
import os
import pytz

# This generates a Excel sheet out of anamnese data
import xlsxwriter

from charm.coach.models import Coach

from django.conf import settings
# This returns the currently active user model
from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from django.utils import timezone

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

class AnamneseDocument(models.Model):
    link = models.CharField(
        null=True, blank=True,
        max_length=256
    )

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

        if not self.date:
            self.date = today

        # Get the raw form data from a submitted anamnese form page
        # json.loads converts it to a dictionary
        content = json.loads(self.form_data)

        try:
            nid = AnamneseDocument.objects.latest('id').id
        except:
            nid = 0

        document_name = 'Anamnese_' \
            + self.user.first_name + '-' \
            + self.user.last_name + '_' \
            + today.strftime("%d/%m/%Y") \
            + '.xlsx'


        directory = settings.AN_DOCUMENT_PATH
        if not os.path.exists(directory):
            os.makedirs(directory)

        path = directory + document_name

        # Create a workbook and add a worksheet.
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet('Anamnesedaten')

        # Add a bold format to use to highlight cells.
        bold = workbook.add_format({'bold': True})
        align_left = workbook.add_format({'align': 'left'})

        # set the column width
        worksheet.set_column('A:A', 39)
        worksheet.set_column('B:B', 66)

        # Write some data headers.
        worksheet.write('A1', '#', bold)
        worksheet.write('B1', 'Antwort', bold)

        # Start from row 1, column 0.
        row = 1
        col = 0

        for k in content:
            # print(k, content[k])
            # print(type(content[k]))
            # print(content[k]['helpText'])
            if k != 'uid':
                worksheet.write(row, col, content[k]['helpText'], bold)
                if type(content[k]['value']) is str or type(content[k]['value']) is int:
                    worksheet.write(row, col+1, content[k]['value'], align_left)
                if type(content[k]['value']) is list:
                    litems = ", "
                    # print(litems.join(content[k]['value']))
                    worksheet.write(row, col+1, litems.join(content[k]['value']), align_left)
                if type(content[k]) is type(None):
                    worksheet.write(row, col+1, "/")
                row += 1

        workbook.close()
        
        alinkcollection = AnamneseDocument(
            link=path
        )

        alinkcollection.save()
        self.document = alinkcollection

        super(Anamnese, self).save(*args, **kwargs)

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

        user_data.update(form.full_values)
        form.full_values = user_data

        an = self.create_an(
            date = timezone.now(),
            user = user,
            coach = form.user,
            form_data = json.dumps(form.full_values, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            an = an,
        )

class AnamneseFormSubmission(AbstractFormSubmission):
    an = models.ForeignKey(Anamnese, on_delete=models.CASCADE)