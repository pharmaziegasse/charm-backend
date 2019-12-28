from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Registration
from ..customer.wagtail_hooks import CustomerAdmin

class RegistrationAdmin(ModelAdmin):
    model = Registration
    menu_label = "Registrations"
    menu_icon = "mail"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the registration overview
    list_display = ('date_joined', 'title', 'first_name', 'last_name', 'email', 'telephone', 'address', 'postal_code', 'city', 'country', 'newsletter')
    search_fields = ('date_joined', 'title', 'first_name', 'last_name', 'email', 'telephone', 'address', 'postal_code', 'city', 'country', 'newsletter')

class CustomerAdminB(ModelAdminGroup):
    menu_label = "Shopify"
    menu_icon = "fa-shopping-basket"
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (
        CustomerAdmin,
        RegistrationAdmin
    )

modeladmin_register(CustomerAdminB)
