from django.contrib.auth.models import User
from django.db import models
from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)


class Profile(models.Model):
    INDUSTRY_CHOICES = (
        ('', '--None--'),
        ('Agriculture', 'Agriculture'),
        ('Apparel', 'Apparel'),
        ('Banking', 'Banking'),
        ('Biotechnology', 'Biotechnology'),
        ('Chemicals', 'Chemicals'),
        ('Communications', 'Communications'),
        ('Construction', 'Construction'),
        ('Consulting', 'Consulting'),
        ('Education', 'Education'),
        ('Electronics', 'Electronics'),
        ('Energy', 'Energy'),
        ('Engineering', 'Engineering'),
        ('Entertainment', 'Entertainment'),
        ('Environmental', 'Environmental'),
        ('Finance', 'Finance'),
        ('Food &amp; Beverage', 'Food &amp; Beverage'),
        ('Government', 'Government'),
        ('Healthcare', 'Healthcare'),
        ('Hospitality', 'Hospitality'),
        ('Insurance', 'Insurance'),
        ('Machinery', 'Machinery'),
        ('Manufacturing', 'Manufacturing'),
        ('Media', 'Media'),
        ('Not For Profit', 'Not For Profit'),
        ('Other', 'Other'),
        ('Recreation', 'Recreation'),
        ('Retail', 'Retail'),
        ('Shipping', 'Shipping'),
        ('Technology', 'Technology'),
        ('Telecommunications', 'Telecommunications'),
        ('Transportation', 'Transportation'),
        ('Utilities', 'Utilities'),
    )

    DEVICE_CHOICES = (
        ('Tablet', 'Tablet'),
        ('Wearable', 'Wearable'),
        ('Other', 'Other'),
    )

    INTEREST_CHOICES = (
        ('Firefox OS', 'Firefox OS'),
        ('Firefox Marketplace', 'Firefox Marketplace'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(User)
    title = models.CharField(max_length=40, blank=True)
    company = models.CharField(max_length=40, blank=True)
    phone = models.CharField(max_length=40, blank=True)
    mobile = models.CharField(max_length=40, blank=True)
    city = models.CharField(blank=True, max_length=40)
    state = models.CharField(blank=True, max_length=40)
    country = models.CharField(blank=True, max_length=40)
    industry = models.CharField(
        blank=True, choices=INDUSTRY_CHOICES, max_length=80)
    type_of_device = models.CharField(
        blank=True, choices=DEVICE_CHOICES, max_length=80)
    mobile_product_interest = models.CharField(
        blank=True, choices=INTEREST_CHOICES, max_length=80)
    description = models.TextField(blank=True)
    salesforce_id = models.CharField(blank=True, max_length=80)
    salesforce_sync = models.BooleanField(default=True)
    last_salesforce_sync = models.DateTimeField(
        blank=True, null=True, db_index=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField(db_index=True)

    def __unicode__(self):
        return unicode(self.user)
