from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Questionnaire_1, Questionnaire_2, Questionnaire_3

class Questionnaire1Admin(ModelAdmin):
    model = Questionnaire_1
    menu_label = "Fragebogen 1"
    menu_icon = "form"
    menu_order = 360

    list_display = (
        'user',
        'coach',
        'form_data'
    )

class Questionnaire2Admin(ModelAdmin):
    model = Questionnaire_2
    menu_label = "Fragebogen 2"
    menu_icon = "form"
    menu_order = 361

    list_display = (
        'user',
        'coach',
        'form_data'
    )

class Questionnaire3Admin(ModelAdmin):
    model = Questionnaire_3
    menu_label = "Fragebogen 3"
    menu_icon = "form"
    menu_order = 362

    list_display = (
        'user',
        'coach',
        'form_data'
    )