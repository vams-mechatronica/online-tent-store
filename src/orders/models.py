from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey("accounts.CustomUser", verbose_name=_("User"), on_delete=models.CASCADE)
    items = models.JSONField(_("Items Ordered"))
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)
    coupon = models.ForeignKey("coupon.Coupon", verbose_name=_("Coupon"), null=True, blank=True, on_delete=models.SET_NULL)
    final_amount = models.DecimalField(_("Final Amount After Discount"), max_digits=10, decimal_places=2, default=0.0)
    booking_amount = models.DecimalField(_("Booking Amount"), max_digits=10, decimal_places=2, default=0.0)
    is_partial_payment_paid = models.BooleanField(_("Is Booking Payment Completed"), default=False)
    is_full_payment_paid = models.BooleanField(_("Is Full Payment Completed"), default=False)
    start_datetime = models.DateTimeField(_("Start Date and Time"))
    end_datetime = models.DateTimeField(_("End Date and Time"))
    hours = models.DecimalField(_("Total Hours"), max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(_("Order Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Order Modified At"), auto_now=True)

    def calculate_hours(self):
        """Calculate hours based on start_datetime and end_datetime."""
        if self.start_datetime and self.end_datetime:
            delta = self.end_datetime - self.start_datetime
            self.hours = delta.total_seconds() / 3600
            return self.hours
        return 0

    def save(self, *args, **kwargs):
        """Override save to calculate hours before saving."""
        self.calculate_hours()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def apply_coupon(self):
        if self.coupon and self.coupon.is_active:
            discount = self.coupon.get_discount_amount(self.total_amount)
            self.final_amount = self.total_amount - discount
        else:
            self.final_amount = self.total_amount
