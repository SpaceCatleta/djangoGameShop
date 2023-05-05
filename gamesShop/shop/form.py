from django import forms
from .models import GameDetail


class AddGameForm(forms.ModelForm):
    class Meta:
        model = GameDetail
        fields = ('cover', 'label', 'developer', 'publisher', 'release_date', 'description')
