# Reference:
# http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Beautyreport


class BeautyreportAdmin(ModelAdmin):
    model = Beautyreport
    menu_label = "Beautyreports"
    menu_icon = "mail"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
   
    # Listed in the customer overview
    list_display = (
        'user',
        'form_data'
        # 'date',
        # 'uid',
        # 'brid',
        )

    search_fields = list_display

modeladmin_register(BeautyreportAdmin)