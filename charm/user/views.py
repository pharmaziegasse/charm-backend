# https://medium.com/@raiderrobert/how-to-make-a-webhook-receiver-in-django-1ce260f4efff

import copy, json, datetime
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import User
# from .models import WebhookTransaction


@csrf_exempt
@require_POST
def webhook(request):
    jsondata = request.body
    data = json.loads(jsondata)
    # meta = copy.copy(request.META)
    
    print(data)
    print(data['addresses'][0])

    user = User(
        gid = data['id'],
        first_name = data['first_name'],
        last_name = data['last_name'],
        email = data['email'],
        telephone = data['phone'],
        orders_count = data['orders_count'],
        total_spent = data['total_spent'],
        note = data['note'],
        coach = User.objects.get(username='simon'),
        address = data['addresses'][0]['address1'],
        city = data['addresses'][0]['city'],
        postal_code = data['addresses'][0]['zip'],
        country = data['addresses'][0]['countryCode']
    )

    user.save()
    print('User Saved')
    

    # WebhookTransaction.objects.create(
    #     date_event_generated=datetime.datetime.fromtimestamp(
    #         data['timestamp']/1000.0, 
    #         tz=timezone.get_current_timezone()
    #     ),
    #     body=data,
    #     request_meta=meta
    # )

    return HttpResponse(status=200)