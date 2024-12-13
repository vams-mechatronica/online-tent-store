from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse


# Create your models here.
class Payment(models.Model):
    order = models.OneToOneField("orders.Order", verbose_name=_("Order"), on_delete=models.CASCADE, related_name="payment")
    advance_amount = models.DecimalField(_("Advance Amount"), max_digits=10, decimal_places=2, default=0.0)
    advance_payment_id = models.CharField(_("Advance Payment ID"), max_length=100, null=True, blank=True)
    advance_payment_transaction_id = models.CharField(_("Advance Payment Transaction ID"), max_length=100, null=True, blank=True)
    pending_amount = models.DecimalField(_("Pending Amount"), max_digits=10, decimal_places=2, default=0.0)
    pending_payment_id = models.CharField(_("Pending Payment ID"), max_length=100, null=True, blank=True)
    pending_payment_transaction_id = models.CharField(_("Pending Payment Transaction ID"), max_length=100, null=True, blank=True)
    advance_date = models.DateTimeField(_("Advance Payment Date"), null=True, blank=True)
    pending_date = models.DateTimeField(_("Pending Payment Date"), null=True, blank=True)

    def __str__(self):
        return f"Payment for Order #{self.order.pk}"
