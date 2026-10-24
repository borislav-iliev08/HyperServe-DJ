from django import forms
from django.core.exceptions import ValidationError
from hyperservedj.mixins import DisabledFormMixin
from restaurants.models import Restaurant, Perks


class RestaurantBaseForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        exclude =['slug']
        widgets={
            'name':forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder':'Enter the restaurant\'s name!'
            }),
            'address':forms.TextInput(attrs={
                'class':'form-control',
                'placeholder':'Enter the restaurant\'s current address!'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control'
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
            'perks':'Choose restaurant\'s benefits!',
            'image':'Upload a restaurant photo (optional).'
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
        description = self.cleaned_data.get('description') or ''
        if len(description.strip()) < 20:
            raise ValidationError('Description must be with at least 20 characters!')
        return description




class RestaurantCreateForm(RestaurantBaseForm):
    class Meta(RestaurantBaseForm.Meta):
        fields = ['name', 'address', 'email', 'image', 'description', 'cuisine_type', 'perks', 'owner']



class RestaurantDeleteForm(DisabledFormMixin,RestaurantBaseForm):
    ...

class RestaurantEditForm(RestaurantBaseForm):
    class Meta(RestaurantBaseForm.Meta):
        exclude = ['slug','owner']




class CreatePerkForm(forms.ModelForm):
    class Meta:
        model = Perks
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Outdoor seating'}),
        }

