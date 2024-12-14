from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class ServiceProvider(models.Model):
    name = models.CharField(_("Service Provider Name"), max_length=5000)
    address = models.TextField(_("Address"))
    contact_person_name = models.CharField(_("Contact Person Name"), max_length=500, null=True, blank=True)
    contact_number = models.CharField(_("Contact number"), max_length=500,null=True, blank=True)
    email = models.EmailField(_("Email Id"), max_length=254,null=True,blank=True)
    
    class Meta:
        verbose_name = _("ServiceProvider")
        verbose_name_plural = _("ServiceProviders")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("ServiceProvider_detail", kwargs={"pk": self.pk})


class SupplierOrder(models.Model):
    order = models.ForeignKey(
        "orders.Order",
        verbose_name=_("Related User Order"),
        on_delete=models.CASCADE,
        related_name="supplier_orders",
    )
    supplier = models.ForeignKey(
        "ServiceProvider",
        verbose_name=_("Supplier"),
        on_delete=models.CASCADE,
        related_name="supplier_orders",
    )
    user = models.ForeignKey(
        "accounts.CustomUser",
        verbose_name=_("User"),
        on_delete=models.CASCADE,
        related_name="supplier_orders",
    )
    items = models.JSONField(
        _("Items Ordered"),
        help_text=_("Details of items supplied by this supplier, including quantities."),
    )
    total_quantity = models.PositiveIntegerField(_("Total Quantity"), default=0)
    total_cost = models.DecimalField(
        _("Total Cost (INR)"), max_digits=10, decimal_places=2, default=0.0
    )
    status = models.CharField(
        _("Order Status"),
        max_length=50,
        choices=[
            ("PENDING", _("Pending")),
            ("IN_PROGRESS", _("In Progress")),
            ("COMPLETED", _("Completed")),
            ("CANCELLED", _("Cancelled")),
        ],
        default="PENDING",
    )
    created_at = models.DateTimeField(_("Order Created At"), auto_now_add=True)
    modified_at = models.DateTimeField(_("Order Modified At"), auto_now=True)

    class Meta:
        verbose_name = _("Supplier Order")
        verbose_name_plural = _("Supplier Orders")
        ordering = ["-created_at"]

    def calculate_total_quantity(self):
        """Calculate the total quantity from the items JSON field."""
        if isinstance(self.items, list):
            self.total_quantity = sum(item.get("quantity", 0) for item in self.items)
        else:
            self.total_quantity = 0
        return self.total_quantity

    def save(self, *args, **kwargs):
        """Override save to calculate total quantity before saving."""
        self.calculate_total_quantity()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Supplier Order #{self.pk} for Supplier {self.supplier.name}"

