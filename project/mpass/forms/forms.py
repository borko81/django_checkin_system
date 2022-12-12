from django import forms

from ..models import PersonInformationModel, CardsModel


class FormatForms:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'    


class PersonForm(FormatForms, forms.ModelForm):
    class Meta:
        model = PersonInformationModel
        fields = 'name group tel picture'.split()



class CardForm(FormatForms, forms.ModelForm):
    class Meta:
        model = CardsModel
        fields = 'card person_id valid_from valid_to is_valid'.split()
        widgets = {
            'valid_to': forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'placeholder':'Select a date', 'type':'date'}),
            'valid_from': forms.DateInput(format=('%Y-%m-%d'), attrs={'class': 'form-control', 'type':'date'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_valid'].widget.attrs['class'] = 'btn'

