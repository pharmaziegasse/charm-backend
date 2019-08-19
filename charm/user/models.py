## Reference:
## http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

from django.contrib.auth.models import AbstractUser

from wagtail.admin.edit_handlers import FieldPanel

# extend AbstractUser Model from django.contrib.auth.models
class User(AbstractUser):
    panels = [
        FieldPanel('username'),
    ]

    def __str__(self):
        return self.username