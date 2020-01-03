import json
import uuid
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel
)
from wagtail.core.fields import StreamField, RichTextField
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, InlinePanel, StreamFieldPanel, MultiFieldPanel, FieldPanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.contrib.forms.models import AbstractForm, AbstractFormField, AbstractEmailForm, AbstractFormField, AbstractFormSubmission
from wagtail.admin.utils import send_mail
from ..user.models import User

# Create your registration related models here.

# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for non-customer datasets based on the User model
        return super(ProxyManager, self).get_queryset().filter(is_active=False)

class Registration(User):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add Registration form
    panels = [
        # FieldPanel('username'),
        FieldPanel('is_customer'),
        FieldPanel('customer_id'),
        FieldPanel('coach'),
        FieldPanel('verified'),
        FieldPanel('title'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('email'),
        FieldPanel('birthdate'),
        FieldPanel('telephone'),
        FieldPanel('address'),
        FieldPanel('city'),
        FieldPanel('postal_code'),
        FieldPanel('country'),
        FieldPanel('newsletter'),
        #FieldPanel('registration_data'),
    ]

    def __str__(self):
        return self.username

    class Meta:
        proxy = True
        ordering = ('date_joined', )


class FormField(AbstractFormField):
    page = ParentalKey('RegistrationformPage', on_delete=models.CASCADE, related_name='form_fields')

class RegistrationformPage(AbstractEmailForm):
    # When creating a new Form page in Wagtail
    registration_head = models.CharField(null=True, blank=False, max_length=255)
    registration_newsletter_text = models.CharField(null=True, blank=False, max_length=255)
    registration_privacy_text = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])
    registration_info_text = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])
    registration_button = models.ForeignKey(
        'home.Button',
        null=True,
        blank=False,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    registration_step_text = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])
    thank_you_text = RichTextField(null=True, blank=False, features=['bold', 'italic', 'underline', 'strikethrough', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'blockquote', 'ol', 'ul', 'hr', 'embed', 'link', 'superscript', 'subscript', 'document-link', 'image', 'code'])

    content_panels = AbstractEmailForm.content_panels + [
      MultiFieldPanel(
          [
            FieldPanel('registration_head', classname="full title"),
            FieldPanel('registration_newsletter_text', classname="full"),
            FieldPanel('registration_privacy_text', classname="full"),
            FieldPanel('registration_info_text', classname="full"),
            FieldPanel('registration_step_text', classname="full"),
            SnippetChooserPanel('registration_button', classname="full"),
            FieldPanel('thank_you_text', classname="full")
          ],
          heading="content",
        ),
      MultiFieldPanel(
          [
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel("subject"),
          ],
          heading="Email Settings"
        ),
      MultiFieldPanel(
        [
          InlinePanel('form_fields', label="Form fields")
        ],
        heading="data",
      )
    ]

    def get_submission_class(self):
        return RegistrationFormSubmission

    # Create a new user
    def create_user(self, title, first_name, last_name, email, telephone, address, city, postal_code, country, newsletter, verified, registration_data):
        # enter the data here
        user = get_user_model()(
            is_active=False,
            is_customer=True,
            title=title,
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            address=address,
            city=city,
            postal_code=postal_code,
            country=country,
            newsletter=newsletter,
            verified=verified,
            registration_data=registration_data,
        )

        user.set_password(str(uuid.uuid4()))
        user.save()

        return user

    # Called when a user registers
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(',')]

        emailheader = "New registration via Pharmaziegasse Website"

        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ', '.join(value)
            content.append('{}: {}'.format(field.label, value))
        content = '\n'.join(content)
        
        content += '\n\nMade with ❤ by Werbeagentur Christian Aichner'

        #emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'
        
        #html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"
        
        send_mail(self.subject, f"{emailheader}\n\n{content}", addresses, self.from_address)
    
    def process_form_submission(self, form):

        user=self.create_user(
          title=form.cleaned_data['title'],
          first_name=form.cleaned_data['first_name'],
          last_name=form.cleaned_data['last_name'],
          email=form.cleaned_data['email'],
          telephone=form.cleaned_data['telephone'],
          address=form.cleaned_data['address'],
          city=form.cleaned_data['city'],
          postal_code=form.cleaned_data['postal_code'],
          country=form.cleaned_data['country'],
          newsletter=form.cleaned_data['newsletter'],
          verified=form.cleaned_data['verified'],
          registration_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)

class RegistrationFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
