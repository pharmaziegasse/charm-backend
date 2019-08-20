# Reference:
# http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Custom User model
from .models import User


class UserAdmin(ModelAdmin):
    model = User
    menu_label = "User"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False
   
    # Listed in the customer overview
    list_display = (
        'date_joined',
        #'username',
        'first_name',
        'last_name',
        'email',
        'telephone',
        )

    search_fields = list_display

modeladmin_register(UserAdmin)