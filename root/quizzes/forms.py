from django import forms
from django.forms.widgets import RadioSelect, Textarea
from .models import Answer


class QuestionForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=RadioSelect)

class QuestionForm2(forms.ModelForm):

    class Meta:
        model = Answer
        fields = ['content']

    # def __init__(self, questions, *args, **kwargs):
    #     super(QuestionForm2, self).__init__(*args, **kwargs)
    #     for question in questions:
    #
    #         choice_list = [("QUESTION TEXT", question.text)]
    #         choice_list.append([(x.pk, x.text) for x in question.get_answers_list()])
    #         self.fields["question-{}".format(question.id)] = forms.ChoiceField(
    #             choices=choice_list,
    #             widget=forms.RadioSelect
    #          )

    def clean_answer(self):
        answer = self.cleaned_data.get('content')
        return answer

