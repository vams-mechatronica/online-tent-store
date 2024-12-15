import requests
from django.conf import settings
from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from .models import *

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


@csrf_exempt
def add_delivery_status(request):
    if request.method == 'POST':
        try:
            results = request.body.get('results')
            for dat in results:
                data = json.loads(dat)
                delivery_status = WhatsappDeliveryStatus(
                    message_id=data['messageId'],
                    to=data['to'],
                    sent_at=parse_datetime(data['sentAt']),
                    done_at=parse_datetime(data['doneAt']),
                    status_id=data['status']['id'],
                    status_group_id=data['status']['groupId'],
                    status_group_name=data['status']['groupName'],
                    status_name=data['status']['name'],
                    status_description=data['status']['description'],
                    error_id=data['error']['id'],
                    error_group_id=data['error']['groupId'],
                    error_group_name=data['error']['groupName'],
                    error_name=data['error']['name'],
                    error_description=data['error']['description'],
                    error_permanent=bool(data['error']['permanent']),
                    price_per_message=data['price']['pricePerMessage'],
                    currency=data['price']['currency']
                )
                delivery_status.save()
            return JsonResponse({"message": "Delivery status added successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def get_delivery_status(request):
    if request.method == 'GET':
        statuses = list(WhatsappDeliveryStatus.objects.values())
        return JsonResponse(statuses, safe=False, status=200)
    return JsonResponse({"error": "Invalid method"}, status=405)

@csrf_exempt
def add_seen_report(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            seen_report = WhatsappSeenReport(
                message_id=data['messageId'],
                sender=data['from'],
                recipient=data['to'],
                sent_at=parse_datetime(data['sentAt']),
                seen_at=parse_datetime(data['seenAt']),
                application_id=data.get('applicationId'),
                entity_id=data.get('entityId')
            )
            seen_report.save()
            return JsonResponse({"message": "Seen report added successfully!"}, status=201)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    return JsonResponse({"error": "Invalid method"}, status=405)
