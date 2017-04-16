from django import forms
from django.forms.widgets import RadioSelect, Textarea
from .models import Answer

class AnswerIDForm(forms.Form):

    # data er det som blir sendt inn fra question.html (answer_id og csfr key)
    # tok bort data som parameter og sender inn som kwargs istedet.
    def __init__(self, sent_in, *args, **kwargs):
        super(AnswerIDForm, self).__init__(*args, **kwargs)

        #answer_id = forms.CharField(widget=forms.RadioSelect)
        #print('answer_id test:')
        #print(answer_id)
        #print('answer_id test slutt:')

        self.fields["answers"] = sent_in.get('answer_id')
        self.fields["questionid"] = sent_in.get('question_id')

        #print(sent_in.get('answer_id'))
        print('Fields fra form:', self.fields)
        print('Answer_id fra form:', self.fields['answers'])
        print('Question_id fra form:', self.fields['questionid'])

    def _clean_fields(self):
        answer_id = self.fields['answers']
        print('answer_id: ', answer_id)
        return answer_id


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

    def __init__(self, guess, *args, **kwargs):
        super(QuestionForm2, self).__init__(*args, **kwargs)
        for question in guess:

            choice_list = [("QUESTION TEXT", question.text)]
            choice_list.append([(x.pk, x.text) for x in question.get_answers_list()])
            self.fields["question-{}".format(question.id)] = forms.ChoiceField(
                choices=choice_list,
                widget=forms.RadioSelect
             )

    def clean_answer(self):
        answer = self.cleaned_data.get('content')
        return answer



