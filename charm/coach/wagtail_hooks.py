from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import Coach

class CoachAdmin(ModelAdmin):
    model = Coach
    menu_label = "Coach"
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
    
modeladmin_register(CoachAdmin)
