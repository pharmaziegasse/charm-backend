# Reference:
# http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

# Custom User model
from .models import User


class UserAdmin(ModelAdmin):
    model = User
    menu_label = "User data"
    menu_icon = "doc-full"
    menu_order = 100
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

# This gets registered with the ModelAdminGroup in the Beautyreport app
# modeladmin_register(UserAdmin)