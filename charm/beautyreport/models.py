import json

from datetime import datetime

from charm.coach.models import Coach

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import connection, models

from django.utils import timezone

from docx import Document
from docx.shared import Inches

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
    # To identify which coach created this beautyreport
    coach = models.ForeignKey(
        Coach, null=True,
        on_delete=models.SET_NULL,
        related_name='Coach_BR'
    )
    # docx_url = models.CharField(
    #     null=True, blank=True,
    #     max_length=128
    # )
    form_data = models.TextField(
        null=True, blank=True
    )

    # custom save function
    def save(self, *args, **kwargs):
        today = datetime.now()
        timezone.make_aware(today)

        if not self.date:
            self.date = today

        # Get the raw form data which got generated out of the submitted anamnese form page
        # json.loads converts it to a dictionary
        content = json.loads(self.form_data)
        # from_data has two fields. A User ID gets sent to identify to whom the beautyreport data belongs and
        # a data field in which the entire generated text (plus user data) is stored as a JSON string.
        # raw_data saves the content of this data field in a seperate variable so that it can be processed further.
        raw_data = content['data']
        # As raw_data is a JSON string again, it must also be converted to a dictionary
        data = json.loads(raw_data)
        
        # Initialize a new document
        document = Document()

        for ka in data:
            # print(data[ka])
            # print("\n-------------\n")
            document.add_heading(data[ka]['chapterHeader'])
            for kb in data[ka]:
                if not kb == 'chapterHeader':
                    # print(data[ka][kb])
                    # print("subChapterHeader:")
                    # print(data[ka][kb]['subChapterHeader'])
                    # print("\n-------------\n")
                    document.add_heading(data[ka][kb]['subChapterHeader'], level=2)
                    for kc in data[ka][kb]:
                        if not kc == 'subChapterHeader':
                            print(data[ka][kb][kc])
                            print("\n-------------\n")
                            try:
                                document.add_paragraph(data[ka][kb][kc]['text'])
                            except:
                                pass

                #print(data[ka][kb])
                # if kb is 'subChapterHeader':
                #     print(data[ka][kb])
                #     break
                #     document.add_paragraph(data[ka][kb])

        # n = 0
        # while True:
        #     try:
        #         document.add_heading(data[str('chapter' + str(n))]['chapterHeader'], level=1)
        #         n1 = 0
        #         while True:
        #             try:
        #                 n2 = 0
        #                 while True:
        #                     try:
        #                         document.add_paragraph(data[str('chapter' + str(n))][str('subchapter' + str(n1))][str('paragraph' + str(n2))]['text'])
        #                         n2 = n2 + 1
        #                     except:
        #                         break
        #                 n1 = n1 + 1
        #             except:
        #                 break
        #         n = n + 1
        #     except:
        #         break



        # document.add_paragraph(data['chapter1']['chapterHeader'])
        # document.add_heading("heading", 0)
        
        document.add_paragraph(self.form_data)
        # p.add_run('bold').bold = True
        # p.add_run(' and some ')
        # p.add_run('italic.').italic = True

        document.add_heading('Heading, level 1', level=1)
        document.add_paragraph('Intense quote', style='Intense Quote')

        document.add_paragraph(
            'first item in unordered list', style='List Bullet'
        )
        document.add_paragraph(
            'first item in ordered list', style='List Number'
        )

        records = (
            (3, '101', 'Spam'),
            (7, '422', 'Eggs'),
            (4, '631', 'Spam, spam, eggs, and spam')
        )

        table = document.add_table(rows=1, cols=3)
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = 'Qty'
        hdr_cells[1].text = 'Id'
        hdr_cells[2].text = 'Desc'
        for qty, id, desc in records:
            row_cells = table.add_row().cells
            row_cells[0].text = str(qty)
            row_cells[1].text = id
            row_cells[2].text = desc

        document.add_page_break()

        document_path = 'documents/Beautyreport-' \
            + self.user.first_name + '-' \
            + today.strftime("%Y-%m-%d") + '-' \
            + str(Beautyreport.objects.latest('id').id + 1) + '.docx'

        document.save('media/' + document_path)

        # This is a cancer cure but it already formed metastases and every hope is too late.
        # https://docs.djangoproject.com/en/2.2/topics/db/sql/
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO wagtaildocs_document (id, title, file, created_at, uploaded_by_user_id, \
                collection_id, file_hash) values (null, 'Beautyreport von ' || %s || ' ' || %s || ' vom ' || %s, %s, datetime(), \
                %s, 1, 'placeholder')",
                [self.user.first_name, self.user.last_name, today.strftime("%d.%m.%Y"), document_path, self.coach.id])

        super(Beautyreport, self).save(*args, **kwargs)

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

    def create_br(self, date, user, coach, form_data):
        br = Beautyreport(
            date = date,
            user = user,
            coach = coach,
            form_data = form_data
        )

        br.save()

        return br

    def process_form_submission(self, form):
        today = datetime.now()
        timezone.make_aware(today)

        br = self.create_br(
            date = today.strftime("%Y-%m-%d %H:%M:%S"),
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