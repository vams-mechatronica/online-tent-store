from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import CustomUserManager
# from products.storage import ProductFileStorage
from datetime import date
from django.utils.translation import gettext_lazy as _
import uuid
from django.contrib.postgres.fields import ArrayField
from django import forms
from django.db.models import Q

# from django.contrib.auth import get_user_model
# User = get_user_model()


#MultiArrayChoiceFields
class ModifiedArrayField(ArrayField):
    def formfield(self, **kwargs):
        defaults = {
            "form_class": forms.MultipleChoiceField,
            "choices": self.base_field.choices,
            "widget": forms.CheckboxSelectMultiple,
            **kwargs
        }
        return super(ArrayField, self).formfield(**defaults)
# Create your models here.
TAGS = (('Home', 'Home'), ('Office',
                                     'Office'), ('Other', 'Other'),)

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('supplier', 'Supplier'),
        ('admin', 'Admin'),
        ('bde', 'Business Development Executives (BDEs)'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES,default='customer')
    first_name = models.CharField(default="Central", max_length=100)
    last_name = models.CharField(default="User", max_length=100)
    email = models.EmailField(null=True,unique=True)
    mobileno = models.CharField(verbose_name="Mobile Number",
                              null=False, max_length=10, default="", unique=True)
    username = models.CharField(null=True, max_length=50, unique=True)
    is_supplier = models.BooleanField(default=False)
    is_mobileverified = models.BooleanField(default=False)
    created_at = models.DateTimeField(_("User Created Date"), auto_now_add=True)
    modified_at = models.DateTimeField(_("User Modified Date"), auto_now=True)
    USERNAME_FIELD: str = 'mobileno'
    REQUIRED_FIELDS: str = ('email',)

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.mobileno

    def user_full_name(self):
        return self.first_name + " " + self.last_name


class UserAddresses(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=_(
        "User Detail"), on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(
        _("contact Name"), max_length=200, blank=True, null=True)
    address = models.CharField(
        _("address"), max_length=200, blank=True, null=True)
    state = models.CharField(
        _("select state"), max_length=200, blank=True, null=True)
    city = models.CharField(
        _("select city"), max_length=200, blank=True, null=True)
    pincode = models.IntegerField(_("address pincode"))
    addPhoneNumber = models.CharField(
        _("address phone number"), max_length=13, null=True, blank=True)
    set_default = models.BooleanField(
        _("Default Address"), null=True, blank=True, default=True)
    email = models.EmailField(_("Contact email"), max_length=254,null=True,blank=True,default="")
    country = models.CharField(
        _("select country"), max_length=200, blank=True, null=True)
    address_type = models.CharField(
        _("Address type"), max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = _("UserAddress")
        verbose_name_plural = _("UserAddress")

    def __str__(self) -> str:
        return "user:{} city: {} pincode: {} phoneno. {}".format(self.user, self.city, self.pincode, self.addPhoneNumber)

    def user_address(self):
        address = self.address if self.address else "" +", "+self.city if self.city else "" +", " + str(self.pincode) if self.pincode else ""
        return address

    # def tag_string(self):
    #     cat = ','.join(i for i in self.tags)
    #     return cat
    
    def save(self, *args, **kwargs):
        if self.set_default:
            self.__class__._default_manager.filter(
                user=self.user, set_default=True).update(set_default=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(set_default=True),
                name='unique_primary_address_per_customer'
            )
        ]

class Country(models.Model):
    country_code = models.CharField(max_length=4, blank=True, null=True)
    country_name = models.CharField(max_length=50, blank=True, null=True)
    nick_name = models.CharField(max_length=5, blank=True, null=True)
    country_image = models.CharField(max_length=200, blank=True, null=True)
    country_image_2 = models.ImageField(upload_to='country', null=True)
    is_top = models.BooleanField(_('is_top'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    created_date = models.DateTimeField(_('created date'), auto_now_add=True)

    def __str__(self):
        return self.country_code


class DeviceOtp(models.Model):
    country = models.ForeignKey(
        Country, related_name='device_country_user', on_delete=models.CASCADE, null=True)
    number = models.CharField(max_length=50, blank=False, null=False)
    otp = models.IntegerField(blank=True, null=True, default=0)
    session = models.CharField(max_length=500, blank=True, null=True)
    status = models.BooleanField(default=False)
    auth_token = models.UUIDField(
        _("auth_token"), null=True, blank=True, default=uuid.uuid4)
    created_date = models.DateTimeField('date created', auto_now_add=True)

    class Meta:
        ordering = ('created_date',)

    def __str__(self):
        return self.number

class Cards(models.Model):
    user = models.ForeignKey(CustomUser, verbose_name=_("User Saved Cards"), on_delete=models.CASCADE)
    card_number = models.CharField(_("Card Number"), max_length=16,null=True,blank=True,default="")
    card_holder_name = models.CharField(
        _("Card Holder Name"), max_length=50, null=True, blank=True, default="")
    exp_month = models.CharField(
        _("Expiry Month"), max_length=50, null=True, blank=True, default="")
    exp_year = models.CharField(
        _("Expiry Year"), max_length=50, null=True, blank=True, default="")
    set_as_default = models.BooleanField(_("Set as default"))

    def save(self, *args, **kwargs):
        if self.set_as_default:
            self.__class__._default_manager.filter(
                user=self.user, set_as_default=True).update(set_as_default=False)
        super().save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'],
                condition=Q(set_as_default=True),
                name='unique_primary_card_per_customer'
            )
        ]
        ordering = ('exp_month', 'exp_year')

        

