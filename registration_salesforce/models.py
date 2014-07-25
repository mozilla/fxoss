from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)


class Profile(models.Model):
    INDUSTRY_CHOICES = (
        ('', _('--None--')),
        ('Agriculture', _('Agriculture')),
        ('Apparel', _('Apparel')),
        ('Banking', _('Banking')),
        ('Biotechnology', _('Biotechnology')),
        ('Chemicals', _('Chemicals')),
        ('Communications', _('Communications')),
        ('Construction', _('Construction')),
        ('Consulting', _('Consulting')),
        ('Education', _('Education')),
        ('Electronics', _('Electronics')),
        ('Energy', _('Energy')),
        ('Engineering', _('Engineering')),
        ('Entertainment', _('Entertainment')),
        ('Environmental', _('Environmental')),
        ('Finance', _('Finance')),
        ('Food &amp; Beverage', _('Food &amp; Beverage')),
        ('Government', _('Government')),
        ('Healthcare', _('Healthcare')),
        ('Hospitality', _('Hospitality')),
        ('Insurance', _('Insurance')),
        ('Machinery', _('Machinery')),
        ('Manufacturing', _('Manufacturing')),
        ('Media', _('Media')),
        ('Not For Profit', _('Not For Profit')),
        ('Other', _('Other')),
        ('Recreation', _('Recreation')),
        ('Retail', _('Retail')),
        ('Shipping', _('Shipping')),
        ('Technology', _('Technology')),
        ('Telecommunications', _('Telecommunications')),
        ('Transportation', _('Transportation')),
        ('Utilities', _('Utilities')),
    )

    DEVICE_CHOICES = (
        ('Tablet', _('Tablet')),
        ('Wearable', _('Wearable')),
        ('Other', _('Other')),
    )

    INTEREST_CHOICES = (
        ('Firefox OS', _('Firefox OS')),
        ('Firefox Marketplace', _('Firefox Marketplace')),
        ('Other', _('Other')),
    )

    user = models.OneToOneField(User)
    title = models.CharField(_('title'), blank=True, max_length=40)
    legal_entity = models.CharField(
        _('legal entity name'), blank=True, max_length=80)
    company = models.CharField(_('company name'), max_length=40)
    company_zip_code = models.CharField(
        _('company zip / postal code'), blank=True, max_length=40)
    website = models.CharField(
        _('company website '), blank=True, max_length=80)
    street = models.CharField(_('street'), blank=True, max_length=80)
    city = models.CharField(_('city'), blank=True, max_length=40)
    state = models.CharField(_('state'), blank=True, max_length=40)
    zip_code = models.CharField(
        _('zip / postal code'), blank=True, max_length=10)
    country = models.CharField(_('country'), blank=True, max_length=40)
    phone = models.CharField(_('phone'), blank=True, max_length=40)
    mobile = models.CharField(_('mobile'), blank=True, max_length=40)
    industry = models.CharField(
        blank=True, choices=INDUSTRY_CHOICES, max_length=80)
    type_of_device = models.CharField(
        blank=True, choices=DEVICE_CHOICES, max_length=80)
    mobile_product_interest = models.CharField(
        blank=True, choices=INTEREST_CHOICES, max_length=80)
    language_preference = models.CharField(
        _('language preference'), blank=True, max_length=40)
    description = models.TextField(_('description'), blank=True)
    salesforce_id = models.CharField(blank=True, max_length=80)
    salesforce_sync = models.BooleanField(default=True)
    last_salesforce_sync = models.DateTimeField(
        blank=True, null=True, db_index=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField(db_index=True)

    def __unicode__(self):
        return unicode(self.user)


class UserNotes(models.Model):
    page = models.OneToOneField(User, editable=False, related_name='extra_fields')
    notes = models.TextField(verbose_name='description', default='', blank=True)
    notes_zh_cn = models.TextField(verbose_name='description', default='', blank=True)
