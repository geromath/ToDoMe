from django.contrib import admin
from .models import Question
from .models import Category
from .models import SubCategory
from .models import Quiz


admin.site.register(Question)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Quiz)