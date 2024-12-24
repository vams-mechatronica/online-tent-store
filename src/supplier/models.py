from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
# from service.models import ServicableAddress


class ServiceProvider(models.Model):
    user = models.OneToOneField("accounts.CustomUser", verbose_name=_("User"),related_name='supplier_profile', on_delete=models.CASCADE)
    name = models.CharField(_("Service Provider Name"), max_length=5000)
    address = models.TextField(_("Address"))
    contact_person_name = models.CharField(_("Contact Person Name"), max_length=500, null=True, blank=True)
    contact_number = models.CharField(_("Contact number"), max_length=500,null=True, blank=True)
    email = models.EmailField(_("Email Id"), max_length=254,null=True,blank=True)
    serviceable_address = models.ManyToManyField("service.ServicableAddress", verbose_name=_("Serviceable Pincode/Address"))
    
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
    items = models.JSONField(
        _("Items Ordered"),
        help_text=_("Details of items supplied by this supplier, including quantities."),
    )
    order_date = models.DateTimeField(_("Ordered On"), auto_now=False, auto_now_add=True, null=True, blank=True)
    event_start_date = models.DateTimeField(_("Event Start Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    event_end_date = models.DateTimeField(_("Event End Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    event_items_delivery_date = models.DateTimeField(_("Event Start Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    event_items_pickup_date = models.DateTimeField(_("Event Start Date"), auto_now=False, auto_now_add=False, null=True, blank=True)
    booking_detail = models.JSONField(_("Booking Details"), help_text=_("Details of Booking, including Customer Details, Address, Event Venue, Time of Booking, Event start date, Event end date, Total Amount, Supplier Share, Payment Status"),default=None)
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


class SupplierTransaction(models.Model):
    # Define statuses as choices
    class TransactionStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        COMPLETED = 'completed', _('Completed')
        FAILED = 'failed', _('Failed')
        CANCELLED = 'cancelled', _('Cancelled')

    supplier = models.ForeignKey('ServiceProvider', on_delete=models.CASCADE, related_name='transactions')
    order = models.ForeignKey("SupplierOrder", related_name="supplier_order", on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)  # Unique transaction reference
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # e.g., 'Bank Transfer', 'UPI', etc.
    status = models.CharField(
        max_length=10,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    remarks = models.TextField(blank=True, null=True)  # Optional field for notes or comments

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.supplier.user.username} ({self.status})"

    class Meta:
        verbose_name = "Supplier Transaction"
        verbose_name_plural = "Supplier Transactions"
        ordering = ['-created_at']


class SupplierAccountDetails(models.Model):
    supplier = models.OneToOneField('ServiceProvider', on_delete=models.CASCADE, related_name='account_details')
    
    # Bank Account Information
    bank_account_number = models.CharField(max_length=20, verbose_name="Bank Account Number")
    bank_name = models.CharField(max_length=100, verbose_name="Bank Name")
    ifsc_code = models.CharField(max_length=11, verbose_name="IFSC Code")  # Standard IFSC length is 11
    micr_code = models.CharField(max_length=9, verbose_name="MICR Code", blank=True, null=True)  # MICR is optional in some cases
    branch_name = models.CharField(max_length=100, verbose_name="Branch Name", blank=True, null=True)

    # UPI Details
    upi_id = models.CharField(max_length=50, verbose_name="UPI ID", blank=True, null=True)

    # Contact Information
    phone_number = models.CharField(max_length=15, verbose_name="Phone Number", blank=True, null=True)

    passbook = models.ImageField(_("Passbook Image"), upload_to='supplier/passbook', height_field=None, width_field=None, max_length=None)

    # Verification and Timestamps
    is_verified = models.BooleanField(default=False, verbose_name="Is Verified?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.supplier.user.username} - Account Details"

    class Meta:
        verbose_name = "Supplier Account Detail"
        verbose_name_plural = "Supplier Account Details"
        ordering = ['-created_at']
