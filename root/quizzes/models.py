from django.db import models

#dette skal vaere en samling av flere spoersmaal
class Questionnaire(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Questionnaire name')
    slug = models.SlugField()


    def __str__(self):
        return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=1000)
    questionnaire = models.ForeignKey(Questionnaire, related_name='questions', on_delete=models.CASCADE,
                                      default="") #relasjon til questionnaire-klassen

    def __str__(self):
        return self.question_text

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE) #relasjon til question-klassen
    answer_text = models.CharField(max_length=200)
    is_valid = models.BooleanField(default=False)

    def __str__(self):
        return self.answer_text



