from django import forms
from .models import Tip


class TipForm(forms.ModelForm):
    class Meta:
        model = Tip
        fields = ['match', 'tip_home', 'tip_guest', 'joker', 'tip_date', 'author']

