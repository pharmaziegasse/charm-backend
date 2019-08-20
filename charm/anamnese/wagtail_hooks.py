from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Anamnese

class AnamneseAdmin(ModelAdmin):
    model = Anamnese
    menu_label = "Anamnese"
    menu_icon = "mail"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
   
    # Listed in the customer overview
    list_display = (
        'user.username',
        'form_data'
        )

    search_fields = list_display

modeladmin_register(AnamneseAdmin)