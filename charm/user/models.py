## Reference:
## http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

# We use uuid to generate a unique username, as Charm's customers are identified by a field other than the username.
import uuid

# AbstractUser is, next to AbstractBaseUser, one of the two default user models in Django.
# AbstractUser already defines some useful fields, which we inherit.
from django.contrib.auth.models import AbstractUser

# The username field uses a validator to check wheter the username value is unique or not.
from django.contrib.auth.validators import UnicodeUsernameValidator

# ValidationError is used to raise our custom errors through the clean() method
from django.core.exceptions import ValidationError

from django.db import models

from wagtail.admin.edit_handlers import FieldPanel

# extend AbstractUser Model from django.contrib.auth.models
class User(AbstractUser):
    # AbstractUser.username field (modified max_length)
    username = models.CharField(
        null=True, blank=True,
        error_messages={'unique': 'A user with that username already exists.'},
        help_text='Required. 36 characters or fewer. Letters, digits and @/./+/-/_ only.',
        max_length=36, unique=True, validators=[UnicodeUsernameValidator()],
        verbose_name='username'
        )
    is_customer = models.BooleanField(
        blank=False, default=True,
        help_text='Establish if the user is a customer'
        )
    is_coach = models.BooleanField(
        blank=False, default=False,
        help_text='Establish if the user is a coach'
        )
    coach = models.CharField(
        null=True, blank=True,
        help_text='If registering a user, set the user\'s coach', max_length=36
        )
    # A secondary "backup" coach is planned to be added later.
    # https://github.com/pharmaziegasse/charm-backend/issues/10
    # secondary_coach = models.CharField(
    #     null=True, blank=True,
    #     help_text='If registering a user, set the user\'s secondary coach', max_length=36
    #     )
    title = models.CharField(
        null=True, blank=True, 
        help_text='Title', max_length=12
    )
    birthdate = models.DateField(
        auto_now=False, auto_now_add=False,
        null=True, blank=True,
        help_text='Birthdate'
    )
    telephone = models.CharField(
        null=True, blank=False, 
        help_text='Phone Number', max_length=40
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

        if (len(ValidationErrorList) > 0):
            # All applicable ValidationErrors get raised
            raise ValidationError([
                ValidationErrorList
            ])

    # custom save function
    def save(self, *args, **kwargs):
        if not User.password:
            # A user must have set a password
            # This has to be done before calling the validation function full_clean()
            User.set_password(self, str(uuid.uuid4()))
        
        # Seems to be checked when logging in to the Wagtail CMS.
        # Therefore raises a ValidationError when superuser is logging in as the dev SU does have an empty phone field.
        # Solution -> Skip check for superuser
        if not User.is_superuser:
            # The full_clean() method calls all three steps involved in validating a model:
            # > Validate the model fields - clean_fields()
            # > Validate the model as a whole - clean(), we defined a custom method of this above
            # > Validate the field uniqueness - validate_unique()
            # https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model.full_clean
            self.full_clean()

        if not self.username:
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

    panels = [
        # FieldPanel('username'),
        FieldPanel('is_customer'),
        FieldPanel('is_coach'),
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