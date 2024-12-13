from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey("accounts.CustomUser", verbose_name=_("User"), on_delete=models.CASCADE)
    items = models.JSONField(_("Items Ordered"))
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)
    coupon = models.ForeignKey("coupon.Coupon", verbose_name=_("Coupon"), null=True, blank=True, on_delete=models.SET_NULL)
    final_amount = models.DecimalField(_("Final Amount After Discount"), max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(_("Order Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Order Modified At"), auto_now=True)

    def __str__(self):
        return f"Order #{self.pk} by {self.user.username}"

    def apply_coupon(self):
        if self.coupon and self.coupon.is_active:
            discount = self.coupon.get_discount_amount(self.total_amount)
            self.final_amount = self.total_amount - discount
        else:
            self.final_amount = self.total_amount
