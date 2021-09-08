import os
from twilio.rest import Client
from django.conf import settings                                                                                                                                                       
from django.http import HttpResponse

# def broadcast_sms(request):
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
# account_sid = os.environ['TWILIO_ACCOUNT_SID']
# auth_token = os.environ['TWILIO_AUTH_TOKEN']
# client = Client(account_sid, auth_token)

# message = client.messages \
#                 .create(
#                      body="Join Earth's mightiest heroes. Like Kevin Bacon.",
#                      from_='+16787014452',
#                      to='+923323161899'
#                  )

# print(message.sid)

def broadcast_sms(request):
    message_to_broadcast = ("gadanchi danna to darahthe marche man tara darkoon kane Regards Ejaz")
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    for recipient in ["+923323161899"]:
        if recipient:
            client.messages.create(to=recipient,
                                   from_=settings.TWILIO_NUMBER,
                                   body=message_to_broadcast)
    return HttpResponse("messages sent!", 200)





    #EdyusEgZJiG_vTHN1KOp0UDNtL50mwZb7QYEc3MI recoverycode