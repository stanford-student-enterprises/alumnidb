from django import forms
from django.conf import settings

class FilterForm(forms.Form):
    is_current = forms.BooleanField()
    is_not_current = forms.BooleanField()
    start_year = forms.ChoiceField(choices=settings.YEAR_CHOICES)
    end_year = forms.ChoiceField(choices=settings.YEAR_CHOICES)