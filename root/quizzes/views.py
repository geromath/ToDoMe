import random

from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import QuestionForm, QuestionForm2, AnswerIDForm
from .models import Quiz, Category, Progress, Sitting, Question, MCQuestion, Answer

from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to the quiz page!")


class QuizMarkerMixin(object):
    @method_decorator(login_required)
    @method_decorator(permission_required('quiz.view_sittings'))
    def dispatch(self, *args, **kwargs):
        return super(QuizMarkerMixin, self).dispatch(*args, **kwargs)

class SittingFilterTitleMixin(object):
    def get_queryset(self):
        queryset = super(SittingFilterTitleMixin, self).get_queryset()
        quiz_filter = self.request.GET.get('quiz_filter')
        if quiz_filter:
            queryset = queryset.filter(quiz__title__icontains=quiz_filter)

        return queryset

class QuizListView(ListView):
    model = Quiz
    template_name = 'quizzes/index_quizzes.html' #lagt til selv. Dette er forsiden man kommer til.

    def get_queryset(self):
        queryset = super(QuizListView, self).get_queryset()
        return queryset.filter(draft=False)


class QuizDetailView(DetailView):

    model = Quiz
    slug_field = 'url'
    template_name = 'quizzes/detail.html'

    def get(self, request, *args, **kwargs): #lagt til id selv: id=None,
         #lagt til selv: self.instance = get_object_or_404(Quiz, id=id)
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
        print(context)
        #lagt til instance selv: instance = self.instance,
        #return self.render_to_response(context)
        return render(request, 'quizzes/detail.html', context)


class CategoriesListView(ListView):
    model = Category


class ViewQuizListByCategory(ListView):
    model = Quiz
    template_name = 'view_quiz_category.html'

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(
            Category,
            category=self.kwargs['category_name']
        )

        return super(ViewQuizListByCategory, self).\
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self)\
            .get_context_data(**kwargs)

        context['category'] = self.category
        return context

    def get_queryset(self):
        queryset = super(ViewQuizListByCategory, self).get_queryset()
        return queryset.filter(category=self.category, draft=False)

class QuizUserProgressView(TemplateView):
    template_name = 'progress.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(QuizUserProgressView, self)\
            .dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(QuizUserProgressView, self).get_context_data(**kwargs)
        progress, c = Progress.objects.get_or_create(user=self.request.user)
        context['cat_scores'] = progress.list_all_cat_scores
        context['exams'] = progress.show_exams()
        return context

class QuizMarkingList(QuizMarkerMixin, SittingFilterTitleMixin, ListView):
    model = Sitting

    def get_queryset(self):
        queryset = super(QuizMarkingList, self).get_queryset()\
                                               .filter(complete=True)

        user_filter = self.request.GET.get('user_filter')
        if user_filter:
            queryset = queryset.filter(user__username__icontains=user_filter)

        return queryset

class QuizMarkingDetail(QuizMarkerMixin, DetailView):
    model = Sitting

    def post(self, request, *args, **kwargs):
        sitting = self.get_object()

        q_to_toggle = request.POST.get('qid', None)
        if q_to_toggle:
            q = Question.objects.get_subclass(id=int(q_to_toggle))
            if int(q_to_toggle) in sitting.get_incorrect_questions:
                sitting.remove_incorrect_question(q)
            else:
                sitting.add_incorrect_question(q)

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super(QuizMarkingDetail, self).get_context_data(**kwargs)
        context['questions'] =\
            context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(FormView):

    form = AnswerIDForm #QuestionForm
    template_name = 'quizzes/question.html'
    #success_url = '/thanks/' #lagt til for å teste
    '''

    #lagt til context for å teste det ut!
    context = {
        'form': form_class
    }


    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug']) #NB: Endret fra 'quiz_name'
        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)

        if self.sitting is False:
            return render(request, 'quizzes/single_complete.html')

        if request.method == "POST": #LAGT til selv for å se hvordan request ser ut
            print(self)
            print(request)
            print(request.POST)
            print(request.POST.get('answer_id'))

            #det under skal kommenteres ut
            form = QuestionForm(request.POST)  # A form bound to the POST data
            if form.is_valid():  # All validation rules pass
                print(form.cleaned_data['answers'])

            #print(self.get_context_data())
            #return QuizTake.form_valid(self, form=QuestionForm(request.POST))



        return super(QuizTake, self).dispatch(request, *args, **kwargs)
    '''

    def get(self, request, *args, **kwargs):
        form = AnswerIDForm

        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])  # NB: Endret fra 'quiz_name'
        progress, created = Progress.objects.get_or_create(user=self.request.user)
        question = [Question.objects.filter(quiz=self.quiz)]

        self.sitting = Sitting.objects.user_sitting(self.request.user,
                                                    self.quiz) #endret fra bare request.user
        # PRØVER UT MED DENNE ISTEDET for question over
        self.question = MCQuestion.objects.get(id=self.sitting.get_first_question().id)

        context = {
            "form": form,
            "quiz": self.quiz,
            "progress": progress,
            "created": created,
            "question": self.question, #la til self. foran
            "sitting": self.sitting,
        }

        print('context in get-method: ', context)


        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)

        if self.sitting is False:
            return render(request, 'quizzes/single_complete.html')

        print('Nå render vi question.html fra GET')
        return render(request, "quizzes/question.html", context)

    def post(self, request, *args, **kwargs):
        print('Nå brukes post-metoden')

        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])  # NB: Endret fra 'quiz_name'
        self.sitting = Sitting.objects.user_sitting(request.user,
                                                       self.quiz)  # endret fra bare request.user

        print('Sjekker score: ', str(self.sitting.get_current_score))
        print('Sjekker maxscore: ', str(self.sitting.get_max_score))
        print('Sjekker om quiz er fullført i starten av post-metoden: ', self.sitting.complete)
        if self.sitting.complete:
            print('Quizen er fullført!')
            return render(self.request, 'quizzes/result.html', {})


        self.form = AnswerIDForm(request.POST, data=request.POST)
        print( 'tilbake i post-metoden')

        self.progress, created = Progress.objects.get_or_create(user=self.request.user)
        self.questions = [Question.objects.filter(quiz=self.quiz)]


        context = {
            "form": self.form,
            "quiz": self.quiz,
            "progress": self.progress,
            "created": created,
            "question": self.questions,
            "sitting": self.sitting,
        }

        print('context i POST: ', context)

        if self.form.is_valid():

            results = self.form_valid(self.form) #la inn variabelen results =

        print('Tilbake i slutten av POST-metoden.')
        print('Sjekker om quiz er fullført i slutten av post-metoden: ', self.sitting.complete)

        #KAN ISTEDET teste bare: if not question_list:
        # return render result.html...

        #Alternativt som vi gjør senere: if self.sitting.get_first_question() is False:
        if not self.sitting.question_list:
            print('Quizen er ferdig og vi skal rendere result.html fra slutten av POST-metoden.')
            return render(self.request, "quizzes/result.html", results) #la til self. foran. Byttet ut context med results


        print('rett før render av question.html i POST-metoden')
        return render(self.request, "quizzes/question.html", context) #la til self. foran


    def get_form(self, form_class=None): #ENDRET fra form_class til form_class=None. OK
        print()
        print('Inn i get_form-metoden.')
        if self.request.user.is_authenticated(): #Endret fra bare self.logged_in_user

            self.question = self.sitting.get_first_question()
            print('neste spørsmål vil være: = ', self.question)
            self.progress = self.sitting.progress()

        return self.get_form_kwargs() #form_class(**self.get_form_kwargs())

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()

        return dict(kwargs, question=self.question)

    def form_valid(self, form): #jeg la ved progress og created også
        print()
        print('Inn i form_valid-metoden.')


        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.form_valid_user(form) #la ved progress og created også

            print('etter form_valid_user')

            if self.sitting.get_first_question() is False:
                print('HIT skal vi etter andre spørsmål')

                return self.final_result_user()
            print('Vi skal hit etter første spørsmål')

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request) #Denne er den opprinnelige. Denne tar oss til get_form-metoden
        #return super(QuizTake, self).form_valid(form)

    def form_valid_user(self, form): #jeg la ved progress og created også
        print()
        print('Inn i form_valid_user-metoden.')
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])  # NB: Endret fra 'quiz_name'

        #self.progress = Progress.objects.get_or_create(user=self.request.user) #Denne var her opprinnelig fremfor å ta i mot som argumenter
        self.progress = Progress.objects.user_progress(self.request.user, self.quiz)

        print('Printer ut self.progress:', self.progress)
        #guess = form.cleaned_data['answers'] #https://docs.djangoproject.com/en/1.10/ref/forms/api/#django.forms.Form.cleaned_data #opprinnelig denne

        #guess = form.cleaned_data.get('answers')
        guess = form.fields['answers']

        #context = self.get_context_data()
        #print('contexten her er nå: ', context)


        questions = MCQuestion.objects.filter(quiz=self.quiz)
        self.sitting = Sitting.objects.user_sitting(self.request.user,
                                                    self.quiz)

        #OBS: DERSOM ikke get_first_question gir neste spørsmål vil det gi logisk feil ved senere retting!!!
        self.question = MCQuestion.objects.get(id=self.sitting.get_first_question().id)
        #NOTE2SELF: dette gir vel neste spørsmål? vi skal vel heller ha gjeldende spørsmål

        #answer = Answer.objects.get(id=guess)
        #self.question = MCQuestion.objects.get(id=)
        print('SJEKK question: ', self.question)

        #print(questions)
        #print(self.request.POST)

        for question in questions:
            print('spm: ', question)
            is_correct = question.check_if_correct(guess)
            if is_correct:
                print('Denne ble true')
                break
            else:
                print('ingen rett svar funnet for dette spørsmålet')

        if is_correct is True:
            self.sitting.add_to_score(1)
            print('Printer ut self.sitting.score:', self.sitting.get_current_score)
            print('TEST: ', self.progress.list_all_cat_scores)
            self.progress.update_score(self.question, 1, 1)

            print('score: ', self.progress.score)

        else:
            print('Legger til INCORRECT_question')
            self.sitting.add_incorrect_question(self.question)
            self.progress.update_score(self.question, 0, 1)

        if self.quiz.answers_at_end is not True:
            self.previous = {'previous_answer': guess,
                             'previous_outcome': is_correct,
                             'previous_question': self.question,
                             'answers': self.question.get_answers(),
                             'question_type': {self.question
                                               .__class__.__name__: True}}
        else:
            self.previous = {}

        self.sitting.add_user_answer(self.question, guess)
        self.sitting.remove_first_question()
        print('removed first question. Length of question_list now: ', len(self.sitting.question_list))
        print('Tester self.sitting funksjoner: ', self.sitting.user_answers)

        print('SLUTT på form_valid_user-metoden')

        #return progress, created #lagt til selv


    def get_context_data(self, **kwargs):
        context = super(QuizTake, self).get_context_data(**kwargs)
        context['question'] = self.question
        context['quiz'] = self.quiz
        if hasattr(self, 'previous'):
            context['previous'] = self.previous
        if hasattr(self, 'progress'):
            context['progress'] = self.progress
        return context

    def final_result_user(self):
        results = {
            'quiz': self.quiz,
            'score': self.sitting.get_current_score,
            'max_score': self.sitting.get_max_score,
            'percent': self.sitting.get_percent_correct,
            'sitting': self.sitting,
            'previous': self.previous,
        }

        print('resultater: ', results)

        self.sitting.mark_quiz_complete()
        print('Ferdig med quiz? ', self.sitting.complete)
        print('Melding på slutten av fullført quiz: ', self.sitting.result_message)

        if self.quiz.answers_at_end:
            results['questions'] =\
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] =\
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            print('Her skjer det noe delete-greier')
            self.sitting.delete()



        print('Nå skal vi til result.html')
        #return render(self.request, 'quizzes/result.html', results) #Denne var her opprinnelig
        return results

