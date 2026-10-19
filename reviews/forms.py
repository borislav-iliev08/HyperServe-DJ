from django import forms
from django.core.exceptions import ValidationError
from .models import Review

class ReviewBaseFrom(forms.ModelForm):
    class Meta:
        model = Review
        exclude =['created_at','is_flagged','restaurant']
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
    ...

class ReviewEditForm(ReviewBaseFrom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].disabled = True

class ReviewDeleteForm(ReviewBaseFrom):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.disabled = True