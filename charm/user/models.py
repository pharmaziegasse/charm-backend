## Reference:
## http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

# We use uuid to generate a unique username, as Charm's customers are identified by a field other than the username.
import uuid

# Json for the form data
import json

# This returns the currently active user model
from django.contrib.auth import get_user_model

# AbstractUser is, next to AbstractBaseUser, one of the two default user models in Django.
# AbstractUser already defines some useful fields, which we inherit.
from django.contrib.auth.models import AbstractUser, Permission

# The username field uses a validator to check wheter the username value is unique or not.
from django.contrib.auth.validators import UnicodeUsernameValidator

# ValidationError is used to raise our custom errors through the clean() method
from django.core.exceptions import ValidationError

# JSON Encoder
from django.core.serializers.json import DjangoJSONEncoder

from django.db import models

from modelcluster.fields import ParentalKey

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField, AbstractFormSubmission

# extend AbstractUser Model from django.contrib.auth.models
class User(AbstractUser):
    # AbstractUser.username field (modified max_length)
    username = models.CharField(
        null=True, blank=True,
        error_messages={'unique': 'A user with that username already exists.'},
        help_text='Set this in case it\'s a staff account',
        max_length=36, unique=True, validators=[UnicodeUsernameValidator()],
        verbose_name='Username / Set this only if it\'s a staff account'
    )
    is_staff = models.BooleanField(
        default=False,
        help_text='Establish if the user is a staff member.'
    )
    is_customer = models.BooleanField(
        blank=False, default=True,
        help_text='Establish if the user is a customer'
    )
    customer_id = models.CharField(
        null=True, blank=True,
        help_text="Kundennummer", max_length=36 
    )
    is_coach = models.BooleanField(
        blank=False, default=False,
        help_text='Establish if the user is a coach'
    )
    # This is called lazy evaluation. https://stackoverflow.com/a/5680864/9638541
    coach = models.ForeignKey(
        'coach.Coach', null=True, blank=True,
        on_delete=models.SET_NULL,
        help_text='Select the user\'s coach'
    )
    # A secondary "backup" coach is planned to be added later. (post-v1.0.0)
    # https://github.com/pharmaziegasse/charm-backend/issues/10
    # secondary_coach = models.CharField(
    #     null=True, blank=True,
    #     help_text='If registering a user, set the user\'s secondary coach', max_length=36
    # )
    title = models.CharField(
        null=True, blank=True, 
        help_text='Title', max_length=20
    )
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False,
        null=True, blank=True,
        help_text='Birthdate'
    )
    telephone = models.CharField(
        null=True, blank=False, unique=True,
        error_messages={'unique': 'A user with that phone number already exists.'},
        help_text='Phone Number', max_length=40
    )
    email = models.EmailField(
        null=True, blank=True,
        help_text='Email Address'
    )
    address = models.CharField(
        null=True, blank=True,
        help_text='Address', max_length=60
    )
    city = models.CharField(
        null=True, blank=True,
        help_text='City', max_length=60
    )
    postal_code = models.CharField(
        null=True, blank=True,
        help_text='Postal Code', max_length=12
    )
    country = models.CharField(
        null=True, blank=True,
        help_text='Country Code (e.g. AT)', max_length=2
    )
    newsletter = models.BooleanField(
        blank=False, default=False,
        help_text='Permit Newsletter'
    )
    registration_data = models.TextField(
        null=True, blank=True,
        help_text='JSON data'
    )
    verified = models.BooleanField(
        blank=False, default=False,
        help_text='Check if the user is verified'
    )
    activation_url = models.CharField(
        null=True, blank=True,
        help_text='Activation URL', max_length=200
    )
    last_password_reset = models.DateTimeField(
        null=True, blank=True,
        help_text='Last password reset'
    )

    # The default identificator Django uses is set to the telephone field
    # USERNAME_FIELD = 'telephone'
    
    # In this method, custom model validation is provided. This is called by full_clean().
    # https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.clean
    def clean(self):
        # ValidationErrors do get saved to the ValidationErrorList Array
        ValidationErrorList = []

        # A user cannot be a customer and a coach at the same time
        if self.is_customer and self.is_coach:
            ValidationErrorList.append(ValidationError("User cannot be customer and coach at the same time"))

        # A customer can not be saved without a coach
        if self.is_customer and not self.coach:
            ValidationErrorList.append(ValidationError("Customer has to have a coach"))

        # A staff member needs a rememberable username to be set to log into the wagtail CMS
        if self.is_staff and not self.username:
            ValidationErrorList.append(ValidationError("Staff member needs a username"))

        # if not self.telephone:
        #     ValidationErrorList.append(ValidationError("User needs to have a valid phone number"))

        if (len(ValidationErrorList) > 0):
            # All applicable ValidationErrors get raised
            raise ValidationError([
                ValidationErrorList
            ])

    # custom save function
    def save(self, *args, **kwargs):
        if not self.password:
            # A user must have set a password
            # This has to be done before calling the validation function full_clean()
            password = str(uuid.uuid4())
            User.set_password(self, password)
            self.activation_url = password

        # Seems to be checked when logging in to the Wagtail CMS.
        # Therefore raises a ValidationError when superuser is logging in as the dev SU does have an empty phone field.
        # Solution -> Skip check for superuser
        if not self.is_superuser:
            # The full_clean() method calls all three steps involved in validating a model:
            # > Validate the model fields - clean_fields()
            # > Validate the model as a whole - clean(), we defined a custom method of this above
            # > Validate the field uniqueness - validate_unique()
            # https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.full_clean
            self.full_clean()

        if not self.is_staff and not self.username:
            # Set the username to a unique, random value
            self.username = str(uuid.uuid4())
            
        if not self.registration_data or self.is_customer:
            if not self.is_active:
                # Sets is_active automatically to True either when registration_data is empty or is_customer is true
                # registration_data is empty when a user is created manually on the Wagtail admin page (coach)
                self.is_active = True
                
                # send_mail(
                #     'got activated',
                #     'You got activated.',
                #     'noreply@pharmaziegasse.at',
                #     ['f.kleber@gasser-partner.at'],
                #     fail_silently=False,
                # )
        else:
            self.is_active = False

        super(User, self).save(*args, **kwargs)

        # Get the coach permission object
        permission = Permission.objects.get(codename='coach')

        if self.is_coach:
            # If the user is a coach, add the coach permission
            self.user_permissions.add(permission)
            # A coach does not have a coach. If a coach is set, it is unset
            self.coach = None
        else:
            self.user_permissions.remove(permission)


    panels = [
        FieldPanel('username'),
        FieldPanel('is_staff'),
        FieldPanel('is_coach'),
        FieldPanel('is_customer'),
        FieldPanel('customer_id'),
        FieldPanel('verified'),
        FieldPanel('coach'),
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
        FieldPanel('activation_url'),
        FieldPanel('last_password_reset'),
        FieldPanel('registration_data'),
    ]

    def __str__(self):
        # Mainly for superusers
        if not self.telephone:
            self.telephone = "Unknown"

        r_string = self.telephone
        if self.first_name or self.last_name or self.email:
            r_string += ":"
        if self.first_name:
            r_string += " " + self.first_name
        if self.last_name:
            r_string += " " + self.last_name
        if self.email:
            if self.first_name or self.last_name:
                r_string += ", " + self.email
            else:
                r_string += " " + self.email

        return r_string


    class Meta:
        # This are custom user permissions in the format "codename": "name"
        permissions = [
            ("coach", "The user is a coach"),
        ]


class FormField(AbstractFormField):
   page = ParentalKey('UserFormPage', on_delete=models.CASCADE, related_name='form_fields')

class UserFormPage(AbstractEmailForm):
    content_panels = AbstractEmailForm.content_panels + [
        MultiFieldPanel(
            [
                InlinePanel('form_fields', label="User form fields")
            ],
            heading="Form Fields",
        )
    ]

    def get_submission_class(self):
        return UserFormSubmission

    def create_user(
        self,
        customer_id,
        coach_id,
        first_name,
        last_name,
        telephone,
        email,
        title,
        birthdate,
        address,
        city,
        postal_code,
        country,
        newsletter,
        registration_data):
        user = User(
            # Next unused ID
            id = User.objects.latest('id').id + 1,

            # Required fields
            first_name = first_name,
            last_name = last_name,
            telephone = telephone,
            email = email,
            coach = User.objects.get(id=coach_id),

            # Optional fields
            customer_id = customer_id,
            title = title,
            birthdate = birthdate,
            address = address,
            city = city,
            postal_code = postal_code,
            country = country,
            newsletter = newsletter,

            # Raw data
            registration_data = registration_data
        )

        user.save()

        return user

    def process_form_submission(self, form):
        user = self.create_user(
            # Required fields
            first_name = form.cleaned_data['first_name'],
            last_name = form.cleaned_data['last_name'],
            telephone = form.cleaned_data['telephone'],
            email = form.cleaned_data['email'],
            coach_id = form.cleaned_data['coach_id'], # Just the ID as an Integer

            # Optional fields
            customer_id = form.cleaned_data['customer_id'],
            title = form.cleaned_data['title'],
            birthdate = form.cleaned_data['birthdate'], # format YYYY-MM-DD or MM/DD/YY its really flexible
            address = form.cleaned_data['address'],
            city = form.cleaned_data['city'],
            postal_code = form.cleaned_data['postal_code'],
            country = form.cleaned_data['country'], # pls send 2 digit country code
            newsletter = form.cleaned_data['newsletter'], # Boolean

            # Raw data
            registration_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder)
        )

        self.get_submission_class().objects.create(
            form_data = json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page = self,
            user = user,
        )

class UserFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(User, on_delete=models.CASCADE)