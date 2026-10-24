from django import forms
from django.core.exceptions import ValidationError
from hyperservedj.mixins import DisabledFormMixin
from .models import Review, EmployeeReview


class ReviewBaseFrom(forms.ModelForm):
    class Meta:
        model = Review
        exclude =['created_at','is_flagged']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author\'s name!'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows':4,
                'placeholder': 'Enter you\'r thoughts!'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter review\'s name!'
            }),
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '0.01'
            }),
        }
        error_messages ={
            'title':{
                'required':"Please enter review\'s title!"
            },
            'content':{
                'required':'Don\'t forget to type you\'r thoughts!'
            },
            'author':{
                'required':'Who say\'s that?'
            }
        }
    def clean_title(self):
        title = self.cleaned_data.get('title')
        bad_words =[
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
        if len(title)< 5:
            raise ValidationError('The title must be at least 5 characters long!')
        for word in bad_words:
            if word in title.lower():
                self.instance.is_flagged = True
        return title



    def clean_content(self):
        content = self.cleaned_data.get('content')
        bad_words =[
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



class ReviewCreateForm(ReviewBaseFrom):
    class Meta(ReviewBaseFrom.Meta):
        exclude =['is_flagged','created_at','restaurant']

class ReviewEditForm(ReviewBaseFrom):
    class Meta(ReviewBaseFrom.Meta):
        exclude =['is_flagged','created_at','restaurant','author']

class ReviewDeleteForm(DisabledFormMixin,ReviewBaseFrom):
    ...


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
            'rating': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1',
                'max': '5',
                'step': '0.01'
            })


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
    class Meta(EmployeeReviewBaseForm.Meta):
        exclude = ['author','is_flagged','created_at','employee']

class EmployeeReviewDeleteForm(DisabledFormMixin,EmployeeReviewBaseForm):
    ...