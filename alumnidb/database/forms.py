from django import forms
from django.conf import settings

class FilterForm(forms.Form):
    is_current = forms.BooleanField(required=False)
    is_not_current = forms.BooleanField(required=False)
    start_year = forms.ChoiceField(choices=[('', '-----')] + (settings.YEAR_CHOICES), required=False)
    end_year = forms.ChoiceField(choices=[('', '-----')] + (settings.YEAR_CHOICES), required=False)