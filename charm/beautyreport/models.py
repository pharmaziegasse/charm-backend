import json

from datetime import datetime

from charm.coach.models import Coach

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder

from django.db import connection, models

from django.utils import timezone

# DOCX or python-docx is used to create and save the Beautyreport as a Word document
from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Inches, Pt, RGBColor

from html.parser import HTMLParser

# GrabzIT is a library for converting HTML text to Word document formatting
# from GrabzIt import GrabzItClient
# from GrabzIt import GrabzItDOCXOptions

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission


class DocumentHTMLParser(HTMLParser):
    def __init__(self, document):
        HTMLParser.__init__(self)
        self.document = document
        # self.paragraph = self.document.add_paragraph()
        # self.run = self.paragraph.add_run()

    def add_paragraph_and_feed(self, html):
        self.paragraph = self.document.add_paragraph()
        self.run = self.paragraph.add_run()
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        # self.run = self.paragraph.add_run()
        if tag == "b":
            self.run.bold = True
        if tag == "i":
            self.run.italic = True
        if tag == "u":
            self.run.underline = True
        if tag in ["br", "ul", "ol"]:
            self.run.add_break()
        if tag == "li":
            self.run.add_text(u'● ')

    def handle_endtag(self, tag):
        if tag in ["br", "li", "ul", "ol"]:
            self.run.add_break()
        if tag == "p":
            self.paragraph = self.document.add_paragraph()
        self.run = self.paragraph.add_run()

    def handle_data(self, data):
        self.run.font.size = Pt(13)
        self.run.font.name = "Oxfam TSTAR PRO"
        self.paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        self.run.add_text(data)
        
    # def handle_starttag(self, tag, attrs):
    #     print("Encountered a start tag:", tag)

    # def handle_endtag(self, tag):
    #     print("Encountered an end tag :", tag)

    # def handle_data(self, data):
    #     print("Encountered some data  :", data)

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
        document = Document("template.docx")

        '''
        # Get default document styles
        styles = document.styles

        # Style for Level 1 Heading
        heading1_style = styles.add_style('L1 Heading', WD_STYLE_TYPE.PARAGRAPH)
        heading1_style.base_style = styles['List Number']
        font = heading1_style.font
        font.size = Pt(16)
        font.bold = True
        font.color.rgb = RGBColor(52, 90, 138)
        font.name = "Oxfam TSTAR PRO Bold"

        # Style for Level 2 Heading
        heading2_style = styles.add_style('L2 Heading', WD_STYLE_TYPE.PARAGRAPH)
        heading2_style.base_style = styles['Heading 2']
        font = heading2_style.font
        font.size = Pt(13)
        font.name = "Oxfam TSTAR PRO Bold"

        # Paragraph Style (spacing)
        paragraph_format = document.styles['Normal'].paragraph_format
        paragraph_format.space_after = 0
        '''

        # document.save("template.docx")

        '''
        # This is a try at translating html myself
        def add_bold(string, p):
            string = string.partition("<b>")
            p.add_run(string[0])
            string = string[2].partition("</b>")
            bold_text = p.add_run(string[0])
            bold_text.bold = True
        
            string_i = bold_text
            while True:
                istr = string[0].find("<i>")
                if istr is not -1:
                    string_i = string_i.partition("<i>")
                    # string_i = string_i[]
                    bold_text.italic = True
                break

            string = string[2]
            return string
        
        def add_italic(string, p):
            string = string.partition("<i>")
            p.add_run(string[0])
            string = string[2].partition("</i>")
            p.add_run(string[0]).italic = True
            string = string[2]
            return string


        def translate_html(document, html):
            p_start = "<p>"
            p_end = "</p>"

            paragraph = html

            while True:
                p = document.add_paragraph()

                paragraph_cache = paragraph.partition(p_start)[2]
                paragraph = paragraph_cache.partition(p_end)[0]

                string = paragraph

                while True:
                    bstr = string.find("<b>")
                    istr = string.find("<i>")

                    if bstr is not -1 or istr is not -1:
                        if bstr is not -1 and istr is -1:
                            string = add_bold(string, p)
                        if bstr is -1 and istr is not -1:
                            string = add_italic(string, p)
                        if bstr is not -1 and istr is not -1:
                            if bstr < istr:
                                string = add_bold(string, p)
                            elif istr < bstr:
                                string = add_italic(string, p)
                    else:
                        p.add_run(string)
                        break

                if paragraph_cache.partition(p_start)[1] is not "<p>":
                    break

                paragraph = paragraph_cache
            
            # text = html
            # text = text.replace("</p><p>", "\r")
            # text = text.replace("<p>", "")
            # text = text.replace("</p>", "")
            return document
        '''

        for ka in data:
            print("**** Word Debugging ****")
            print("*** Chapter:")
            print(data[ka])
            print("--------------------------------------------------")
            #document.add_heading(str(idx) + " " + data[ka]['chapterHeader'])
            document.add_paragraph(data[ka]['chapterHeader'], style='L1 Heading')
            print("--------------------------------------------------")
            print("*** Adding Heading:")
            print(data[ka]['chapterHeader'])
            print("--------------------------------------------------")
            for kb in data[ka]:
                if not kb == 'chapterHeader':
                    if not data[ka][kb]['subChapterHeader'] == '':
                        document.add_paragraph(data[ka][kb]['subChapterHeader'], style='L2 Heading')
                    print("--------------------------------------------------")
                    print("*** Adding Sub Heading:")
                    print(data[ka][kb]['subChapterHeader'])
                    print("--------------------------------------------------")
                    for kc in data[ka][kb]:
                        if not kc == 'subChapterHeader':
                            print("--------------------------------------------------")
                            print("*** Adding Paragraph:")
                            print(data[ka][kb][kc])
                            print("--------------------------------------------------")
                            try:
                                parser = DocumentHTMLParser(document)
                                parser.add_paragraph_and_feed(data[ka][kb][kc]['text'])
                                print("* Sucessfully added Paragraph")
                                print("--------------------------------------------------")
                            except:
                                print("* Failed adding Paragraph")
                                print("--------------------------------------------------")
                                pass
            # Page break after main chapter
            lb = document.add_paragraph()
            lb.add_run().add_break(WD_BREAK.PAGE)



        # '''

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