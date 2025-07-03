from django import forms
from .models import JobApplication

class AddJobForm(forms.ModelForm):
    class Meta: #Meta is a special inner class used to define metadata 
        model=JobApplication
        fields=['company_name', 'position', 'application_date', 'status']
        widgets = {
            'company_name': forms.TextInput(attrs={ 
                'class': 'form-control', #Gives a clean input field style via Bootstrap
                'required': True #Ensures the browser shows a "Please fill out this field" warning if empty
            }),
            'position': forms.TextInput(attrs={
                'class': 'form-control',
                'required': True
            }),
            'application_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'required': True
            }),
            'status': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
        }

#identify duplicate entries at the time of adding jobs and neglecting it
    def clean(self):
        cleaned_data=super().clean()
        company=cleaned_data.get('company_name')
        position=cleaned_data.get('position')

        if JobApplication.objects.filter(company_name=company, position=position).exists():
            raise forms.ValidationError("You already added this job application.")
        
        return cleaned_data