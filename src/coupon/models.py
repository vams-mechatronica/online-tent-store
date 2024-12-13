from django.db import models
from django.utils.translation import gettext_lazy as _
# from django.contrib.auth import get_user_model
from django.urls import reverse

class Coupon(models.Model):
    code = models.CharField(_("Coupon Code"), max_length=50, unique=True)
    discount_percentage = models.DecimalField(_("Discount Percentage"), max_digits=5, decimal_places=2)
    max_discount_amount = models.DecimalField(_("Maximum Discount Amount"), max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField(_("Valid From"))
    valid_to = models.DateTimeField(_("Valid To"))
    is_active = models.BooleanField(_("Is Active"), default=True)

    def __str__(self):
        return f"{self.code} - {self.discount_percentage}%"

    def get_discount_amount(self, total_amount):
        discount = (total_amount * self.discount_percentage) / 100
        if self.max_discount_amount:
            discount = min(discount, self.max_discount_amount)
        return discount
