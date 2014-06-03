from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import mail_admins
from django.db.models import F, Q
from django.utils import timezone
from simple_salesforce import Salesforce
from simple_salesforce.api import SalesforceMalformedRequest

from .models import Profile


LEAD_FIELDS = [
    'Id', 'IsDeleted', 'MasterRecordId', 'LastName', 'FirstName',
    'Salutation', 'Name', 'Title', 'Company', 'Street', 'City', 'State',
    'PostalCode', 'Country', 'Latitude', 'Longitude', 'Phone', 'Email',
    'Website', 'Description', 'LeadSource', 'Status', 'Industry', 'Rating',
    'AnnualRevenue', 'NumberOfEmployees', 'OwnerId', 'IsConverted',
    'ConvertedDate', 'ConvertedAccountId', 'ConvertedContactId',
    'ConvertedOpportunityId', 'IsUnreadByOwner', 'CreatedDate',
    'CreatedById', 'LastModifiedDate', 'LastModifiedById', 'SystemModstamp',
    'LastActivityDate', 'LastViewedDate', 'LastReferencedDate', 'JigsawContactId',
    'EmailBouncedReason', 'EmailBouncedDate', 'Interest__c', 'Type_of_Device__c',
    'MobileProductInterest__c']


LEAD_USER = {
    'FirstName': 'first_name',
    'LastName': 'last_name',
    'Email': 'email'
}


LEAD_PROFILE = {
    'Title': 'title',
    'Company': 'company',
    'Phone': 'phone',
    #TODO: create 'Mobile' column in salesforce lead
    'City': 'city',
    'State': 'state',
    'Country': 'country',
    'Industry': 'industry',
    'Type_of_Device__c': 'type_of_device',
    'MobileProductInterest__c': 'mobile_product_interest',
    'Description': 'description',
    'Id': 'salesforce_id',
}


def salesforce():
    return Salesforce(**settings.SALESFORCE)


def lead_field_names(sf=None):
    """Should return a list matching LEAD_FIELDS"""
    sf = sf or salesforce()
    return [f['name'] for f in sf.Lead.describe()['fields']]


def salesforce_id_from_email(email, sf=None):
    sf = sf or salesforce()
    response = sf.query("select Id from Lead where Email = '%s'" % email)
    for lead in response['records']:
        return lead['Id']


def update(instance, **kwargs):
    return instance._default_manager.filter(pk=instance.pk).update(**kwargs)


def create_profile_from_lead(user, lead):
    profile = Profile.objects.create(
        user=user,
        **{profile_field: lead[sf_field]
           for sf_field, profile_field in LEAD_PROFILE.items()
           if lead.get(lead_field)})
    update(profile, last_salesforce_sync=timezone.now())


def get_leads(sf=None):
    sf = sf or salesforce()
    response = sf.query_all(
        """
        select {} from Lead
        where LeadSource = 'mobilepartners.mozilla.org' and Email != ''
        """.format(', '.join(LEAD_PROFILE.keys() + ['Email'])))
    return response['records'] # TODO: error handling


def create_profiles_from_leads(leads=None, sf=None):
    sf = sf or salesforce()
    for lead in (leads or get_leads(sf)):
        users = User.objects.filter(email=lead['Email'])[:1]
        if users:
            create_profile_from_lead(users[0], lead)


def lead_data(profile):
    data = {'LeadSource': 'mobilepartners.mozilla.org'}
    for sf_field, profile_field in LEAD_PROFILE.items():
        value = getattr(profile, profile_field, None)
        if value and sf_field != 'Id':
            data[sf_field] = value
    for sf_field, user_field in LEAD_USER.items():
        value = getattr(profile.user, user_field , None)
        if value:
            data[sf_field] = value
    return data


def create_leads(profiles, sf=None):
    sf = sf or salesforce()
    for profile in filter(lambda p: p.salesforce_sync, profiles):
        try:
            result = sf.Lead.create(lead_data(profile))
        except SalesforceMalformedRequest as e:
            if 'INVALID_EMAIL' in e.message:
                update(profile, salesforce_sync=False)
                continue
            else:
                raise e
        if not (result['success'] and result['id']):
            raise SalesforceError(
                'Failed to create Lead for {}'.format(profile))
        update(profile, salesforce_id=result['id'],
               last_salesforce_sync=timezone.now())


def update_leads(profiles, sf=None):
    sf = sf or salesforce()
    for profile in filter(lambda p: p.salesforce_sync, profiles):
        sf.Lead.update(profile.salesforce_id, lead_data(profile))
        update(profile, last_salesforce_sync=timezone.now())


def get_salesforce_ids(profiles, sf=None):
    sf = sf or salesforce()
    for profile in profiles:
        salesforce_id = salesforce_id_from_email(profile.user.email)
        if salesforce_id:
            update(profile, salesforce_id=salesforce_id)


def sync_leads_from_profiles(sf=None):
    sf = sf or salesforce()
    profiles = Profile.objects.filter(salesforce_sync=True)
    create_leads(profiles.filter(salesforce_id=''), sf)
    update_leads(profiles.exclude(salesforce_id='').filter(
                 last_salesforce_sync__lt=F('modified')), sf)


class SalesforceError(Exception):
    pass
