from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class ServicableAddress(models.Model):
    area = models.CharField(_("Area/Sector"), max_length=500)
    city = models.CharField(_("City/District"), max_length=500)
    state = models.CharField(_("State"), max_length=100)
    pincode = models.IntegerField(_("Pincode"),default=123456)
    
    class Meta:
        verbose_name = _("Servicable Address")
        verbose_name_plural = _("Servicable Addresss")

    def __str__(self):
        return "{}, {}, {} - {}".format(self.area,self.city,self.state,self.pincode)

    def get_absolute_url(self):
        return reverse("ServicableAddress_detail", kwargs={"pk": self.pk})