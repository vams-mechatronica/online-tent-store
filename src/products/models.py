from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# import
from supplier.models import ServiceProvider


# Create your models here.
class Category(models.Model):
    name = models.CharField(_("Category Name"), max_length=500)
    image = models.ImageField(_("Category Image"), upload_to='Category/', height_field=None, width_field=None, max_length=None)
    created_at = models.DateTimeField(_("Created At"), auto_now=True, auto_now_add=False)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=False, auto_now_add=True)
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Category")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Category_detail", kwargs={"pk": self.pk})

class Product(models.Model):
    name = models.CharField(_("Product Name"), max_length=500)
    category = models.ForeignKey("Category", verbose_name=_("Category Name"), on_delete=models.CASCADE)
    supplier = models.ForeignKey("supplier.ServiceProvider", verbose_name=_("Supplier"), on_delete=models.SET_NULL, null=True,blank=True)
    size = models.CharField(_("Product Size"), max_length=50, null=True, blank=True)
    unit = models.CharField(_("Product Size Unit"), max_length=50, null=True, blank=True)
    unit_base_price = models.IntegerField(_("Product Base Price per hour in INR"), default=10)
    minimum_quantity = models.IntegerField(_("Product Order Minimum Required Quantity"),default=1)
    quantity = models.PositiveIntegerField(_("Quantity"),default=1)
    created_at = models.DateTimeField(_("Created At"), auto_now=True, auto_now_add=False)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product_detail", kwargs={"pk": self.pk})

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='Product/',max_length=500)
    created_at = models.DateTimeField(_("Created At"), auto_now=True, auto_now_add=False)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} Image"
    
    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")

class GatheringSize(models.Model):
    name = models.CharField(_("Gathering Size"), max_length=500)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)
    
    class Meta:
        verbose_name = _("GatheringSize")
        verbose_name_plural = _("GatheringSizes")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("GatheringSize_detail", kwargs={"pk": self.pk})

class PartyingForChoice(models.Model):
    name = models.CharField(_("Name"), max_length=500)
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)
    class Meta:
        verbose_name = _("PartyingForChoice")
        verbose_name_plural = _("PartyingForChoices")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("PartyingForChoice_detail", kwargs={"pk": self.pk})


class UserRequirement(models.Model):
    user = models.ForeignKey("accounts.CustomUSer", verbose_name=_("User"), on_delete=models.CASCADE)
    partying_for = models.ForeignKey("PartyingForChoice", verbose_name=_("Partying For"), on_delete=models.CASCADE,null=True,blank=True)
    gathering_of = models.ForeignKey("GatheringSize", verbose_name=_("Gathering For"), on_delete=models.CASCADE,null=True,blank=True)
    plot_area = models.CharField(_("Plot Area (in feets)"), max_length=500,null=True,blank=True)
    description = models.TextField(_("Description"))
    created_at = models.DateTimeField(_("Created At"), auto_now=False, auto_now_add=True)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=True, auto_now_add=False)

    class Meta:
        verbose_name = _("UserRequirement")
        verbose_name_plural = _("UserRequirements")

    def __str__(self):
        return self.user

    def get_absolute_url(self):
        return reverse("UserRequirement_detail", kwargs={"pk": self.pk})



