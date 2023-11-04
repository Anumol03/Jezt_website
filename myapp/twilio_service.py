
from twilio.rest import Client
from django.conf import settings

# twilio_service.py
from twilio.rest import Client
from django.conf import settings

def send_sms(to, body, from_):
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        message = client.messages.create(
            to=to,
            from_=from_,
            body=body
        )

        return message.sid
    except Exception as e:
        # Log the error or print it for debugging
        print(f"Error sending SMS: {e}")
        raise  # Re-raise the exception for the caller to handle

# Rest of your twilio_service.py file


def send_sms(to, body):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        to=to,
        from_=settings.TWILIO_PHONE_NUMBER,
        body=body
    )

    return message.sid
