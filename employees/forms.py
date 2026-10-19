import re

from django import forms
from django.core.exceptions import ValidationError

from .models import Employee,EmployeeReview

class EmployeeBaseForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude =['restaurant','rating']
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

class EmployeeDeleteForm(EmployeeBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True






class EmployeeReviewBaseForm(forms.ModelForm):
    class Meta:
        model =EmployeeReview
        exclude =['employee','created_at','is_flagged']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter review\'s name!'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter you\'r thoughts!'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author\'s name!'
            }),


        }
        error_messages = {
            'title': {
                'required': "Please enter review\'s title!"
            },
            'content': {
                'required': 'Don\'t forget to type you\'r thoughts!'
            },
            'author': {
                'required': 'Who say\'s that?'
            }
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        bad_words = [
                'fuck',
                'fucking',
                'shit',
                'bitch',
                'bastard',
                'asshole',
                'crap',
                'idiot',
                'stupid',
                'gay',
                'lesbian',
                'trans',
                'faggot']
        for word in bad_words:
            if word in content.lower():
                self.instance.is_flagged = True
        return content


class EmployeeReviewCreateForm(EmployeeReviewBaseForm):
    ...

class EmployeeReviewEditForm(EmployeeReviewBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True

class EmployeeReviewDeleteForm(EmployeeReviewBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True