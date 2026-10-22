class DisabledFormMixin:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['disabled'] = 'disabled'
            field.widget.attrs['readonly'] = 'readonly'