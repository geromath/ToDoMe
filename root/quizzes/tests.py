from django.test import TestCase
from .models import Category, SubCategory


class TestCategory(TestCase):

    def setUp(self):
        self.c1 = Category.objects.new_category(category='vodka')
        self.sub1 = SubCategory.objects.create(sub_category='absolute', category=self.c1)

    def test_categories(self):
        self.assertEqual(self.c1.category, 'vodka')

    def test_sub_categories(self):
        self.assertEquals(self.sub1.category, self.c1)


