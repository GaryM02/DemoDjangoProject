from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
   class Meta:
     model = Project
     fields = ('vendor', 'client', 'name', 'description', 'duration', 'startdate', 'completiondate', 'cost', 'status')
     widgets = {
         'vendor': forms.TextInput(attrs={
             'class':'form-control'
         }),
         'client': forms.TextInput(attrs={
             'class':'form-control'
         }),
         'name': forms.TextInput(attrs={
             'class':'form-control'
         }),
         'description': forms.Textarea(attrs={
             'class':'form-control'
         }),
         'duration': forms.TextInput(attrs={
             'class':'form-control'
         }),
         'startdate': forms.DateInput(attrs={
             'class':'form-control'
         }),
         'completiondate': forms.DateInput(attrs={
             'class':'form-control'
         }),
         'cost': forms.TextInput(attrs={
             'class':'form-control'
         }),

     }