from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


class WhatsappChat(models.Model):
    
    

    class Meta:
        verbose_name = _("WhatsappChat")
        verbose_name_plural = _("WhatsappChats")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("WhatsappChat_detail", kwargs={"pk": self.pk})



from django.db import models

class WhatsAppInboundMessage(models.Model):
    # Sender Information
    sender_number = models.CharField(max_length=15, help_text="Phone number of the sender")
    sender_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the sender (if available)")

    # Message Details
    message_id = models.CharField(max_length=255, unique=True, help_text="Unique ID of the message from Infobip")
    message_content = models.TextField(help_text="Content of the WhatsApp message")
    message_type = models.CharField(
        max_length=50, 
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('audio', 'Audio'),
            ('location', 'Location'),
            ('contact', 'Contact'),
            ('sticker', 'Sticker'),
            ('other', 'Other')
        ],
        default='text',
        help_text="Type of the message"
    )

    # Timestamp
    received_at = models.DateTimeField(help_text="Timestamp when the message was received")

    # Metadata
    metadata = models.JSONField(blank=True, null=True, help_text="Additional metadata for the message")

    # Status and Flags
    processed = models.BooleanField(default=False, help_text="Flag to mark if the message has been processed")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record update timestamp")

    def __str__(self):
        return f"Message from {self.sender_number} ({self.message_type})"

    class Meta:
        verbose_name = "WhatsApp Inbound Message"
        verbose_name_plural = "WhatsApp Inbound Messages"
        ordering = ['-received_at']

    def __str__(self):
        return self.message_id

    def get_absolute_url(self):
        return reverse("WhatsAppInboundMessage_detail", kwargs={"pk": self.pk})


class WhatsAppOutboundMessage(models.Model):
    # Recipient Information
    recipient_number = models.CharField(max_length=15, help_text="Phone number of the recipient")
    recipient_name = models.CharField(max_length=255, blank=True, null=True, help_text="Name of the recipient (if available)")

    # Message Details
    message_id = models.CharField(max_length=255, unique=True, help_text="Unique ID of the message from Infobip (if available)")
    message_content = models.TextField(help_text="Content of the WhatsApp message")
    message_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('audio', 'Audio'),
            ('location', 'Location'),
            ('contact', 'Contact'),
            ('sticker', 'Sticker'),
            ('template', 'Template'),
            ('other', 'Other')
        ],
        default='text',
        help_text="Type of the message"
    )

    # Status and Metadata
    status = models.CharField(
        max_length=50,
        choices=[
            ('pending', 'Pending'),
            ('sent', 'Sent'),
            ('delivered', 'Delivered'),
            ('read', 'Read'),
            ('failed', 'Failed'),
        ],
        default='pending',
        help_text="Status of the outbound message"
    )
    metadata = models.JSONField(blank=True, null=True, help_text="Additional metadata for the message")

    # Timestamps
    sent_at = models.DateTimeField(blank=True, null=True, help_text="Timestamp when the message was sent")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Record creation timestamp")
    updated_at = models.DateTimeField(auto_now=True, help_text="Record update timestamp")

    def __str__(self):
        return f"Message to {self.recipient_number} ({self.message_type}) - {self.status}"

    class Meta:
        verbose_name = "WhatsApp Outbound Message"
        verbose_name_plural = "WhatsApp Outbound Messages"
        ordering = ['-created_at']


