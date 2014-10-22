from django import forms


class ExportForm(forms.Form):
    export_since = forms.DateField()
