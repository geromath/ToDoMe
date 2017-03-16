from django.test import TestCase
from .models import Category, SubCategory, Quiz, Question, MCQuestion, Answer

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




