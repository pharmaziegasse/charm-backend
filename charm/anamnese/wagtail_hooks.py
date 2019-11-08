from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Anamnese, AnamneseDocument

class AnamenseLinks(ModelAdmin):
    model = AnamneseDocument
    menu_label = "Anamnese Links"
    menu_icon = "link"
    menu_order = 310

    list_display = (
        'link',
    )

class AnamneseAdmin(ModelAdmin):
    model = Anamnese
    menu_label = "Anamneses"
    menu_icon = "form"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
   
    # Listed in the customer overview
    list_display = (
        'user',
        'coach',
        'form_data'
        )

    search_fields = list_display

# This gets registered with the ModelAdminGroup in the Beautyreport app
# modeladmin_register(AnamneseAdmin)