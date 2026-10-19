from django import forms
from django.core.exceptions import ValidationError
from restaurants.models import Restaurant


class RestaurantBaseForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude =['slug','rating']
        widgets={
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter the restaurant\'s name!'
            }),
            'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter the restaurant\'s current address!'
            }),
            'email':forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter restaurant\'s email (e.g. restaurant@gmail.com)'
            }),
            'description':forms.Textarea(attrs={
                'class':'form-control',
                'rows':4,
                'placeholder':'Short description for the place!'
            }),
            'cuisine_type':forms.Select(attrs={
                'class':'form-select'
            }),
            'perks':forms.CheckboxSelectMultiple(),
            'owner':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Owner\'s name!'
            })

        }
        help_texts ={
            'perks':'Choose restaurant\'s benefits!'
        }
        error_messages = {
            'name':{
                'required':'Please enter restaurant\'s name!',
                'unique':'There is another restaurant with this name!',
                'max_length':'Too long!'
            },
            'address':{
                'required': 'Please enter restaurant\'s address!',
                'max_length':'Too long!',
                'unique':'Another restaurant is in this location!'

            },
            'email':{
                'required': 'Please enter an email address!',
                'invalid': 'Please enter a valid email address!',
                'unique': 'An restaurant with this email already exists!'
            }
            ,
            'description':{
                'required': 'Please enter restaurant\'s description!'
            },
            'cuisine_type':{
                'required': 'Please select restaurant\'s cuisine!'
            },
            'owner':{
                'required': 'Please enter restaurant\'s owner!'
            }

        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name)<5:
            raise ValidationError('Restaurant\'s name must be at least 5 symbols long!')
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description)< 20:
            raise ValidationError('Description must be with at least 20 characters!')
        return description



class RestaurantCreateForm(RestaurantBaseForm):
    ...

class RestaurantDeleteForm(RestaurantBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.disabled = True

class RestaurantEditForm(RestaurantBaseForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['owner'].disabled =True


