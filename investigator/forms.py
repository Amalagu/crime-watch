from django import forms
from .models import Case, Report




class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['title', 'category', 'description', 'reporter', 'incident_date', 'incident_time', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={'id': 'report-title', 'required': True}),
            'category': forms.Select(attrs={'id': 'category', 'required': True}),
            'description': forms.Textarea(attrs={'id': 'description', 'cols': '30', 'rows': '10', 'required': True, 'class': 'resize-none outline-none border-2 py-1 px-2 rounded focus:border-blue-500'}),
            'reporter': forms.TextInput(attrs={'id': 'reporter', 'required': True, 'placeholder': 'Enter your name'}),
            'incident_date': forms.DateInput(attrs={'id': 'incident-date', 'type': 'date', 'required': True}),
            'incident_time': forms.TimeInput(attrs={'id': 'incident-time', 'type': 'time', 'required': True}),
            'photo': forms.FileInput(attrs={'id': 'evidence'}),
        }




class CaseForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ['report', 'investigator', 'authorization_letter']
