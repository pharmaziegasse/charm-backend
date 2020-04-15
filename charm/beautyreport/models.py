import json
import os
import pytz

from charm.coach.models import Coach

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from django.conf import settings
from django.utils import timezone

# DOCX or python-docx is used to create and save the Beautyreport as a Word document
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.shared import Inches, Pt, RGBColor
from docx.text.tabstops import TabStop, TabStops

from .document import handle_word

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

class BeautyreportDocument(models.Model):
    # Stores the absolute path to a beautyreport
    link = models.CharField(
        null=True, blank=True,
        max_length=256
    )

class FormField(AbstractFormField):
    page = ParentalKey('BrFormPage', on_delete=models.CASCADE, related_name='form_fields')

class Beautyreport(models.Model):
    # Creation date and time of the beauty report
    date = models.DateTimeField(
        null=True, blank=True
    )

    # To identify to which user the anamnese report belongs to
    user = models.ForeignKey(
        get_user_model(), null=True,
        on_delete=models.SET_NULL
    )

    # To identify which coach created this beautyreport
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_BR'
    )

    # Save the correlating object which stores the beauty report's link
    document = models.ForeignKey(
        BeautyreportDocument,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='Document_BR'
    )

    # Clean HTML data of which the beauty report is generated
    form_data = models.TextField(
        null=True, blank=True
    )

    # custom save function
    def save(self, *args, **kwargs):
        today = timezone.now()

        # Set the creation date
        if not self.date:
            self.date = today

        # Create the MS Word document
        document = handle_word(self.form_data)

        # Save the document in following format
        # Generating two beauty reports for the same person on the same day will intentially override the older one
        document_name = 'Beautyreport_' \
            + self.user.first_name + '-' \
            + self.user.last_name + '_' \
            + today.strftime("%d-%m-%Y") \
            + '.docx'

        # In the settings file, the path for saving beauty report word documents is set with the BR_DOCUMENT_PATH variable
        # Get the document path, and, if the folder does not exist already, create it
        directory = settings.BR_DOCUMENT_PATH
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Get the document's path
        path = directory + document_name

        # Save the Word document
        document.save(path)

        # Create an object for storing the beauty report's link
        blinkcollection = BeautyreportDocument(
            link=path
        )

        blinkcollection.save()

        # Create the relation between the beauty report data's object and the link to the beauty report
        self.document = blinkcollection

        super(Beautyreport, self).save(*args, **kwargs)

    class Meta:
        get_latest_by = "date"


class BrFormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="Beautyreport field")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return BeautyreportFormSubmission

    def create_br(self, user, coach, form_data):
        br = Beautyreport(
            user = user,
            coach = coach,
            form_data = form_data
        )

        br.save()

        return br

    def process_form_submission(self, form):
        br = self.create_br(
            user = get_user_model().objects.get(id=form.cleaned_data['uid']),
            coach = form.user,
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            br = br,
        )


class BeautyreportFormSubmission(AbstractFormSubmission):
    br = models.ForeignKey(Beautyreport, on_delete=models.CASCADE)
