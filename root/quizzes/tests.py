# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User, Permission
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template import Template, Context
from django.test import TestCase
from django.utils.module_loading import import_module
from django.utils.six import StringIO
from .models import Category, SubCategory, Quiz, Question, MCQuestion, Answer, Progress, Sitting
from .views import QuizListView, CategoriesListView, QuizDetailView

class TestCategory(TestCase):

    def setUp(self):
        self.c1 = Category.objects.new_category(category='vodka')
        self.sub1 = SubCategory.objects.create(sub_category='absolute', category=self.c1)

    def test_categories(self):
        self.assertEqual(self.c1.category, 'vodka')

    def test_sub_categories(self):
        self.assertEquals(self.sub1.category, self.c1)

class TestQuiz(TestCase):

    def setUp(self):
        self.c1 = Category.objects.new_category(category='drinks')
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='url1')
        self.quiz2 = Quiz.objects.create(id=2,
                                        title='test quiz 2',
                                        description='d2',
                                        url='url 2')
        self.quiz3 = Quiz.objects.create(id=3,
                                         title='test quiz 3',
                                         description='d3',
                                         url='test url  3')
        self.quiz4 = Quiz.objects.create(id=4,
                                         title='test quiz 4',
                                         description='d4',
                                         url='T-!£$%^&*Q4')
        self.question1 = MCQuestion.objects.create(id=1,
                                                   content='beste finske vodkaen')
        self.question1.quiz.add(self.quiz1)

    def test_quiz_url(self):
        self.assertEqual(self.quiz1.url, 'url1')
        self.assertEqual(self.quiz2.url, 'url-2')
        self.assertEqual(self.quiz3.url, 'test-url-3')
        self.assertEqual(self.quiz4.url, 't-q4')

    def test_quiz_options(self):
        q5 = Quiz.objects.create(id=5,
                                 title='test quiz 5',
                                 description='d5',
                                 url='tq5',
                                 category=self.c1,
                                 exam_paper=True)

        self.assertEqual(q5.category.category, self.c1.category)
        self.assertEqual(q5.random_order, False)
        self.assertEqual(q5.answers_at_end, False)
        self.assertEqual(q5.exam_paper, True)

    def test_quiz_single_attempt(self):
        self.quiz1.single_attempt = True
        self.quiz1.save()

        self.assertEqual(self.quiz1.exam_paper, True)

    def test_get_max_score(self):
        self.assertEqual(self.quiz1.get_max_score, 1)

    def test_get_questions(self):
        self.assertIn(self.question1, self.quiz1.get_questions())

    def test_pass_mark(self):
        self.assertEqual(self.quiz1.pass_mark, False)
        self.quiz1.pass_mark = 50
        self.assertEqual(self.quiz1.pass_mark, 50)
        self.quiz1.pass_mark = 101
        with self.assertRaises(ValidationError):
            self.quiz1.save()

class TestProgress(TestCase):
    def setUp(self):
        self.c1 = Category.objects.new_category(category='elderberries')

        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='tq1')

        self.question1 = MCQuestion.objects.create(content='squawk',
                                                   category=self.c1)

        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@jacob.com',
                                             password='top_secret')

        self.p1 = Progress.objects.new_progress(self.user)

    def test_list_all_empty(self):
        self.assertEqual(self.p1.score, '')

        category_dict = self.p1.list_all_cat_scores

        self.assertIn(str(list(category_dict.keys())[0]), self.p1.score)

        self.assertIn(self.c1.category, self.p1.score)

        Category.objects.new_category(category='cheese')

        self.p1.list_all_cat_scores

        self.assertIn('cheese', self.p1.score)

    def test_subcategory_all_empty(self):
        SubCategory.objects.create(sub_category='pickles',
                                   category=self.c1)
        # self.p1.list_all_cat_scores
        # self.assertIn('pickles', self.p1.score)
        # TODO: test after implementing subcategory scoring on progress page

    def test_update_score(self):
        self.p1.list_all_cat_scores
        self.p1.update_score(self.question1, 1, 2)
        self.assertIn('elderberries', self.p1.list_all_cat_scores)

        cheese = Category.objects.new_category(category='cheese')
        question2 = MCQuestion.objects.create(content='squeek',
                                              category=cheese)
        self.p1.update_score(question2, 3, 4)

        self.assertIn('cheese', self.p1.list_all_cat_scores)
        self.assertEqual([3, 4, 75], self.p1.list_all_cat_scores['cheese'])

        # pass in string instead of question instance
        with self.assertRaises(AttributeError):
            self.p1.update_score('hamster', 3, 4)

        non_int = self.p1.update_score(question2, '1', 2)
        self.assertIn('error', str(non_int))

        # negative possible score
        self.p1.update_score(question2, 0, -1)
        self.assertEqual([3, 5, 60], self.p1.list_all_cat_scores['cheese'])

        # negative added score
        self.p1.update_score(question2, -1, 1)
        self.assertEqual([4, 6, 67], self.p1.list_all_cat_scores['cheese'])

class TestSitting(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='tq1',
                                         pass_mark=50,
                                         success_text="Well done",
                                         fail_text="Bad luck")

        self.question1 = MCQuestion.objects.create(id=1,
                                                   content='squawk')
        self.question1.quiz.add(self.quiz1)

        self.answer1 = Answer.objects.create(id=123,
                                             question=self.question1,
                                             content='bing',
                                             correct=False)

        self.question2 = MCQuestion.objects.create(id=2,
                                                   content='squeek')
        self.question2.quiz.add(self.quiz1)

        self.answer2 = Answer.objects.create(id=456,
                                             question=self.question2,
                                             content='bong',
                                             correct=True)

        self.user = User.objects.create_user(username='jacob',
                                             email='jacob@jacob.com',
                                             password='top_secret')

        self.sitting = Sitting.objects.new_sitting(self.user, self.quiz1)
    '''
    def test_max_questions_subsetting(self):
        quiz2 = Quiz.objects.create(id=2,
                                    title='test quiz 2',
                                    description='d2',
                                    url='tq2',
                                    )
        self.question1.quiz.add(quiz2)
        self.question2.quiz.add(quiz2)
        sub_sitting = Sitting.objects.new_sitting(self.user, quiz2)

        self.assertNotIn('2', sub_sitting.question_list)
    '''

    def test_get_next_remove_first(self):
        self.assertEqual(self.sitting.get_first_question(),
                         self.question1)

        self.sitting.remove_first_question()
        self.assertEqual(self.sitting.get_first_question(),
                         self.question2)

        self.sitting.remove_first_question()
        self.assertEqual(self.sitting.get_first_question(), False)

        self.sitting.remove_first_question()
        self.assertEqual(self.sitting.get_first_question(), False)

    def test_scoring(self):
        self.assertEqual(self.sitting.get_current_score, 0)
        self.assertEqual(self.sitting.check_if_passed, False)
        self.assertEqual(self.sitting.result_message, 'Bad luck')

        self.sitting.add_to_score(1)
        self.assertEqual(self.sitting.get_current_score, 1)
        self.assertEqual(self.sitting.get_percent_correct, 50)

        self.sitting.add_to_score(1)
        self.assertEqual(self.sitting.get_current_score, 2)
        self.assertEqual(self.sitting.get_percent_correct, 100)

        self.sitting.add_to_score(1)
        self.assertEqual(self.sitting.get_current_score, 3)
        self.assertEqual(self.sitting.get_percent_correct, 100)

        self.assertEqual(self.sitting.check_if_passed, True)
        self.assertEqual(self.sitting.result_message, 'Well done')

    def test_incorrect_and_complete(self):
        self.assertEqual(self.sitting.get_incorrect_questions, [])

        self.sitting.add_incorrect_question(self.question1)
        self.assertIn(1, self.sitting.get_incorrect_questions)

        #question3 = TF_Question.objects.create(id=3,
        #                                       content='oink')
        #self.sitting.add_incorrect_question(question3)
        #self.assertIn(3, self.sitting.get_incorrect_questions)

        self.assertEqual(self.sitting.complete, False)
        self.sitting.mark_quiz_complete()
        self.assertEqual(self.sitting.complete, True)

        self.assertEqual(self.sitting.current_score, 0)
        self.sitting.add_incorrect_question(self.question2)
        self.assertEqual(self.sitting.current_score, -1)

    def test_add_user_answer(self):
        guess = '123'
        self.sitting.add_user_answer(self.question1, guess)

        self.assertIn('123', self.sitting.user_answers)

    def test_return_questions_with_answers(self):
        '''
        Also tests sitting.get_questions(with_answers=True)
        '''
        self.sitting.add_user_answer(self.question1, '123')
        self.sitting.add_user_answer(self.question2, '456')

        user_answers = self.sitting.questions_with_user_answers
        self.assertEqual('123', user_answers[self.question1])
        self.assertEqual('456', user_answers[self.question2])

    def test_remove_incorrect_answer(self):
        self.sitting.add_incorrect_question(self.question1)
        self.sitting.add_incorrect_question(self.question2)
        self.sitting.remove_incorrect_question(self.question1)
        self.assertEqual(self.sitting.incorrect_questions, '2')
        self.assertEqual(self.sitting.current_score, 1)

    def test_return_user_sitting(self):
        via_manager = Sitting.objects.user_sitting(self.user, self.quiz1)
        self.assertEqual(self.sitting, via_manager)

    def test_progress_tracker(self):
        self.assertEqual(self.sitting.progress(), (0, 2))
        self.sitting.add_user_answer(self.question1, '123')
        self.assertEqual(self.sitting.progress(), (1, 2))

class TestNonQuestionViews(TestCase):
    '''
    Starting on views not directly involved with questions.
    '''
    urls = 'quiz.urls'

    def setUp(self):
        self.c1 = Category.objects.new_category(category='elderberries')
        self.c2 = Category.objects.new_category(category='straw.berries')
        self.c3 = Category.objects.new_category(category='black berries')

        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='tq1',
                                         category=self.c1,
                                         single_attempt=True)
        self.quiz2 = Quiz.objects.create(id=2,
                                         title='test quiz 2',
                                         description='d2',
                                         url='t q2')
'''
    def test_index_with_drafts(self):
        self.quiz3 = Quiz.objects.create(id=3,
                                         title='test quiz 3',
                                         description='draft',
                                         url='draft',
                                         draft=True)

        self.assertEqual(len(self.view.get_quizzes_done()), 0)
        self.assertEqual(len(self.view.get_quizzes_not_done()), 2)
'''

'''
    def test_index(self):
        # unit
        view = QuizListView()
        self.assertEqual(view.get_queryset().count(), 2)

        # integration test
        response = self.client.get('/')
        self.assertContains(response, 'test quiz 1')
        self.assertTemplateUsed('quiz_list.html')
'''

'''
    def test_list_categories(self):
        # unit
        view = CategoriesListView()
        self.assertEqual(view.get_queryset().count(), 3)

        # integration test
        response = self.client.get('/category/')

        self.assertContains(response, 'elderberries')
        self.assertContains(response, 'straw.berries')
        self.assertContains(response, 'black-berries')

    def test_view_cat(self):
        # unit
        view = CategoriesListView()
        self.assertEqual(view.get_queryset().count(), 3)

        # integration test
        response = self.client.get('/category/elderberries/')

        self.assertContains(response, 'test quiz 1')
        self.assertNotContains(response, 'test quiz 2')
'''

'''
    def test_progress_user(self):
        user = User.objects.create_user(username='jacob',
                                        email='jacob@jacob.com',
                                        password='top_secret')
        question1 = MCQuestion.objects.create(content='squawk',
                                              category=self.c1)

        self.client.login(username='jacob', password='top_secret')
        p1 = Progress.objects.new_progress(user)
        p1.update_score(question1, 1, 2)

        response = self.client.get('/progress/')

        self.assertContains(response, 'elderberries')
        self.assertIn('straw.berries', response.context['cat_scores'])
        self.assertEqual([1, 2, 50],
                         response.context['cat_scores']['elderberries'])

    def test_quiz_start_page(self):
        # unit
        view = QuizDetailView()
        view.kwargs = dict(slug='tq1')
        self.assertEqual(view.get_object().category, self.c1)

        # integration test
        response = self.client.get('/tq1/')

        self.assertContains(response, 'd1')
        self.assertContains(response, 'attempt')
        self.assertContains(response, 'href="/tq1/take/"')
        self.assertTemplateUsed(response, 'quiz/quiz_detail.html')
'''

class TestQuestionMarking(TestCase):
    urls = 'quiz.urls'

    #Maa lages naar vi har lagd views

'''
class TestQuestion(TestCase):
    def setUp(self):
        self.quiz1 = Quiz.objects.create(id=1,
                                         title='test quiz 1',
                                         description='d1',
                                         url='url1')
        self.c1 = Category.objects.new_category(category='testcategory')
        self.sub1 = SubCategory.objects.create(sub_category='testsub', category=self.c1)
        self.q1 = Question.objects.create(id=1,
                                          quiz=self.quiz1,
                                          category=self.c1,
                                          sub_category=self.sub1,
                                          #content='Dette er en test',
                                          #explanation='Dette er forklaringen'
                                          )

    def test_create_question(self):
        self.assertEqual(self.q1.quiz, self.quiz1)
        self.assertEqual(self.q1.category, self.c1)
        self.assertEqual(self.q1.sub_category, self.sub1)
        #self.assertEqual(self.q1.content, 'Dette er en test')
        #self.assertEqual(self.q1.explanation, 'Dette er forklaringen')

'''
