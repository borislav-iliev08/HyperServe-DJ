import re

from django import forms
from django.core.exceptions import ValidationError

from hyperservedj.mixins import DisabledFormMixin
from .models import Employee

class EmployeeBaseForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ['restaurant']
        widgets ={
            'first_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter employee\'s first name!'
            }),
            'last_name':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter employee\'s last name!'
            }),
            'email':forms.EmailInput(attrs={
                'class':'form-control',
                'placeholder':'Enter employee\'s email (e.g. john@gmail.com)'
            }),
            'phone_number':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter employee\'s phone number!'
            }),
            'profile_picture':forms.ClearableFileInput(attrs={
                'class': 'form-control',

            }),
        }
        help_texts ={
            'profile_picture':'Upload employee\'s profile picture!'
        }
        error_messages = {
            'first_name': {
                'required': 'Please enter employee\'s first name!',
            },
            'last_name': {
                'required': 'Please enter employee\'s last name!',
            },
            "email":{
                'required':'Please enter employee\'s email!',
                'invalid':'Please enter valid email!',

            }
            ,
            'phone_number': {
                'required': 'Please provide a phone number!',
                'unique': 'This phone number is already registered for another employee!'
            },
            'profile_picture': {
                'invalid_image': 'Please upload a valid image file.',
            }
        }



    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if not re.match(r'^\+?[\d\s\-]{8,20}$', phone):
            raise ValidationError('Please enter a valid phone number (digits, spaces, and "+" allowed)!')

        return phone



class EmployeeCreateForm(EmployeeBaseForm):
    ...

class EmployeeEditForm(EmployeeBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['profile_picture'].widget = forms.FileInput(attrs={
            'class': 'form-control employee-photo-input',
            'accept': 'image/*',
        })
    class Meta(EmployeeBaseForm.Meta):
        exclude = ['restaurant']

class EmployeeDeleteForm(DisabledFormMixin,EmployeeBaseForm):
    ...


