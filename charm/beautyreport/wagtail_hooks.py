# Reference:
# http://docs.wagtail.io/en/v2.6.1/reference/contrib/modeladmin/

from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register

from .models import Beautyreport, BeautyreportDocument
from ..anamnese.wagtail_hooks import AnamneseAdmin
from ..user.wagtail_hooks import UserAdmin

class BeautyreportLinks(ModelAdmin):
    model = BeautyreportDocument
    menu_label = "Beautyreport Links"
    menu_icon = "link"
    menu_order = 300

    list_display = (
        'link',
    )

class BeautyreportAdmin(ModelAdmin):
    model = Beautyreport
    menu_label = "Beautyreports"
    menu_icon = "folder-inverse"
    menu_order = 300
    add_to_settings_menu = False
    exclude_from_explorer = False
   
    # Listed in the customer overview
    list_display = (
        'user',
        'coach',
        'form_data'
        # 'date',
        # 'uid',
        # 'brid',
        )

    search_fields = list_display

class DataGroup(ModelAdminGroup):
    menu_label = "Data Group"
    menu_icon = "doc-empty-inverse"
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (UserAdmin, AnamneseAdmin, BeautyreportAdmin, BeautyreportLinks)

modeladmin_register(DataGroup)