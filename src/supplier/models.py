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

