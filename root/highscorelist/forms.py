__author__ = 'caroline1'

from django import forms


class ScoreForm(forms.ModelForm):
    user_id = forms.IntegerField(required=True, help_text="The id of the user")
    score = forms.IntegerField(required=True, help_text="Score as positive integer")

    class Participants:  # info
        fields = ['username', 'score']
