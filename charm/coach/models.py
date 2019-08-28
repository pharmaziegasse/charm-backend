from django.contrib.auth.models import BaseUserManager

from wagtail.admin.edit_handlers import FieldPanel

from charm.user.models import User

# Model manager to use in Proxy model
class ProxyManager(BaseUserManager):
    def get_queryset(self):
        # filter the objects for activate customer datasets based on the User model
        return super(ProxyManager, self).get_queryset().filter(is_coach=True)

class Coach(User):
    # call the model manager on user objects
    objects = ProxyManager()

    # Panels/fields to fill in the Add Customer form
    panels = [
        FieldPanel('username'),
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
        proxy = True
        ordering = ('date_joined', )