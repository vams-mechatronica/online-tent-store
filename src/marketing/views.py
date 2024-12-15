import requests
from django.conf import settings
from django.http import JsonResponse
from .models import WhatsAppOutboundMessage

def send_whatsapp_message(recipient_number, message_content, message_type='text'):
    # Infobip API endpoint and credentials
    api_url = "https://api.infobip.com/whatsapp/1/message"
    headers = {
        "Authorization": f"App {settings.INFOBIP_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "to": recipient_number,
        "type": message_type,
        "text": {"body": message_content} if message_type == 'text' else None
        # Add other message types (e.g., images, documents) as per Infobip API specs
    }

    # Save the outbound message to the database
    outbound_message = WhatsAppOutboundMessage.objects.create(
        recipient_number=recipient_number,
        message_content=message_content,
        message_type=message_type,
        status='pending'
    )

    try:
        # Send the message via Infobip
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()

        if response.status_code == 200:
            outbound_message.status = 'sent'
            outbound_message.message_id = response_data.get('messageId')
        else:
            outbound_message.status = 'failed'

        # Save response metadata
        outbound_message.metadata = response_data
        outbound_message.sent_at = timezone.now()
        outbound_message.save()

        return JsonResponse({"status": "success", "data": response_data}, status=200)
    except Exception as e:
        # Update the message status in case of an error
        outbound_message.status = 'failed'
        outbound_message.metadata = {"error": str(e)}
        outbound_message.save()

        return JsonResponse({"status": "error", "message": str(e)}, status=500)



from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import WhatsAppInboundMessage

@csrf_exempt
def whatsapp_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            WhatsAppInboundMessage.objects.create(
                sender_number=data['from'],
                sender_name=data.get('contact', {}).get('name'),
                message_id=data['messageId'],
                message_content=data.get('text', {}).get('body', ''),
                message_type=data.get('type', 'text'),
                received_at=data['timestamp'],
                metadata=data
            )
            return JsonResponse({"status": "success"}, status=201)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error", "message": "Invalid request method"}, status=405)
