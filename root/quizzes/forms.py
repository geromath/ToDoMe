from django import forms
from django.forms.widgets import RadioSelect, Textarea
from .models import Answer

class AnswerIDForm(forms.Form):

    # sent_in er det som blir sendt inn fra question.html (answer_id og csfr key)

    def __init__(self, sent_in, *args, **kwargs):
        super(AnswerIDForm, self).__init__(*args, **kwargs)

        self.fields["answers"] = sent_in.get('answer_id')
        self.fields["questionid"] = sent_in.get('question_id')

    def _clean_fields(self):
        answer_id = self.fields['answers']
        print('answer_id: ', answer_id)
        return answer_id



