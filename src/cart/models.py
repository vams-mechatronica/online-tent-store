from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Wishlist(models.Model):
    user = models.ForeignKey("accounts.CustomUser", verbose_name=_("User"), on_delete=models.CASCADE)
    item = models.ForeignKey("products.Product", verbose_name=_("Product"), on_delete=models.SET_NULL,null=True,blank=True)
    quantity = models.PositiveIntegerField(_("Quantity"),default=1)
    ordered = models.BooleanField(_("Ordered"),default=False)
    created_at = models.DateTimeField(_("Created At"), auto_now=True, auto_now_add=False)
    modified_at = models.DateTimeField(_("Modified At"), auto_now=False, auto_now_add=True)

    class Meta:
        verbose_name = _("Wishlist")
        verbose_name_plural = _("Wishlists")

    def __str__(self):
        return f"Wishlist #{self.pk}: {self.user.username} - {self.item.name if self.item else 'No Product'}"

    def get_absolute_url(self):
        return reverse("Wishlist_detail", kwargs={"pk": self.pk})

