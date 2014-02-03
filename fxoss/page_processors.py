from django import forms
from django.http import HttpResponseRedirect

from mezzanine.pages.page_processors import processor_for


class AgreementForm(forms.Form):
    agreement = forms.BooleanField()

    def clean(self):
        cleaned_data = super(AgreementForm, self).clean()

        if not cleaned_data.get('agreement'):
            raise forms.ValidationError("You must agree to the TOS to access the branding assets.")


# Decorate for supplied slug
@processor_for('test-form')
def branding_assets_agreement_form(request, page):
    form = AgreementForm()
    if request.method == "POST":
        form = AgreementForm(request.POST)
        if form.is_valid():
            # Form processing goes here.
            redirect = request.path
            return HttpResponseRedirect(redirect)
    return {"form": form}
