import django.forms as forms

class CmuxSearchForm(forms.Form):
    text = forms.CharField(required=False)