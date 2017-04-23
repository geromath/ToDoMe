from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView, ListView, TemplateView, FormView

from .forms import AnswerIDForm
from .models import Quiz, Category, Progress, Sitting, Question, MCQuestion


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
    template_name = 'quizzes/index_quizzes.html'  # lagt til selv. Dette er forsiden man kommer til.

    def get_quizzes_not_done(self, **kwargs):
        quizzes = Quiz.objects.all()
        sittings = Sitting.objects.filter(user=self.request.user)
        sittings_list = []
        for sit in sittings:
            sittings_list.append(str(sit.quiz.title))

        quizzes_not_done = []
        for quiz in quizzes:
            if str(quiz) not in sittings_list:
                quizzes_not_done.append(quiz)
        return quizzes_not_done

    def get_quizzes_done(self):
        sittings = Sitting.objects.filter(user=self.request.user)
        sittings_list = []
        for sit in sittings:
            sittings_list.append(sit.quiz)
        return sittings_list

    def get_start_time(self):
        sitting = Sitting.objects.filter(user=self.request.user)[:1].get()
        return sitting.start


class QuizDetailView(DetailView):
    model = Quiz
    slug_field = 'url'
    template_name = 'quizzes/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        if self.object.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        context = self.get_context_data(object=self.object)
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

        return super(ViewQuizListByCategory, self). \
            dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ViewQuizListByCategory, self) \
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
        return super(QuizUserProgressView, self) \
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
        queryset = super(QuizMarkingList, self).get_queryset() \
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
        context['questions'] = \
            context['sitting'].get_questions(with_answers=True)
        return context


class QuizTake(FormView):
    form = AnswerIDForm
    template_name = 'quizzes/question.html'

    def get(self, request, *args, **kwargs):
        form = AnswerIDForm

        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])
        progress, created = Progress.objects.get_or_create(user=self.request.user)

        self.sitting = Sitting.objects.user_sitting(self.request.user,
                                                    self.quiz)

        self.question = MCQuestion.objects.get(id=self.sitting.get_first_question().id)

        context = {
            "form": form,
            "quiz": self.quiz,
            "progress": progress,
            "created": created,
            "question": self.question,
            "sitting": self.sitting,
        }

        if self.quiz.draft and not request.user.has_perm('quiz.change_quiz'):
            raise PermissionDenied

        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.sitting = Sitting.objects.user_sitting(request.user,
                                                        self.quiz)
        if self.sitting is False:
            return render(request, 'quizzes/single_complete.html')

        return render(request, "quizzes/question.html", context)

    def post(self, request, *args, **kwargs):
        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])
        self.sitting = Sitting.objects.user_sitting(request.user,
                                                    self.quiz)

        self.form = AnswerIDForm(request.POST, data=request.POST)
        self.progress, created = Progress.objects.get_or_create(user=self.request.user)
        self.questions = [Question.objects.filter(quiz=self.quiz)]

        if self.form.is_valid():
            results = self.form_valid(self.form)

        if not self.sitting.question_list:
            return render(self.request, "quizzes/result.html", results)

        context = {
            "form": self.form,
            "quiz": self.quiz,
            "progress": self.progress,
            "created": created,
            "question": self.questions,
            "sitting": self.sitting,
        }

        return render(self.request, "quizzes/question.html", context)

    def get_form(self, form_class=None):
        if self.request.user.is_authenticated():
            self.question = self.sitting.get_first_question()
            self.progress = self.sitting.progress()

        return self.get_form_kwargs()

    def get_form_kwargs(self):
        kwargs = super(QuizTake, self).get_form_kwargs()
        return dict(kwargs, question=self.question)

    def form_valid(self, form):
        self.logged_in_user = self.request.user.is_authenticated()

        if self.logged_in_user:
            self.form_valid_user(form)

            if self.sitting.get_first_question() is False:
                return self.final_result_user()

        self.request.POST = {}

        return super(QuizTake, self).get(self, self.request)

    def form_valid_user(self, form):

        self.quiz = get_object_or_404(Quiz, url=self.kwargs['slug'])
        self.progress = Progress.objects.user_progress(self.request.user, self.quiz)
        guess = form.fields['answers']
        questions = MCQuestion.objects.filter(quiz=self.quiz)
        self.sitting = Sitting.objects.user_sitting(self.request.user,
                                                    self.quiz)
        self.question = MCQuestion.objects.get(id=self.sitting.get_first_question().id)

        for question in questions:
            is_correct = question.check_if_correct(guess)
            if is_correct:
                break

        if is_correct is True:
            self.sitting.add_to_score(1)
            self.progress.update_score(self.question, 1, 1)
        else:
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
            'progress': self.progress
        }

        self.sitting.mark_quiz_complete()

        if self.quiz.answers_at_end:
            results['questions'] = \
                self.sitting.get_questions(with_answers=True)
            results['incorrect_questions'] = \
                self.sitting.get_incorrect_questions

        if self.quiz.exam_paper is False:
            self.sitting.delete()

        return results
