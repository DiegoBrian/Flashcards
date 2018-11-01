from django.urls import path

from . import words
from . import expressions
from . import index

urlpatterns = [
	path('', index.index, name = 'index'),
    path('words', words.index, name='words'),
    path('add1min/<int:word_number>', words.sum_1min, name='sum_1min'),
    path('add10min/<int:word_number>', words.sum_10min, name='sum_10min'),
    path('add4days/<int:word_number>', words.sum_4days, name='sum_4days'),
    path('expressions', expressions.index, name='expressions'),
    path('expressions/add1min/<int:expression_number>', expressions.sum_1min, name='sum1min'),
    path('expressions/add10min/<int:expression_number>', expressions.sum_10min, name='sum10min'),
    path('expressions/add4days/<int:expression_number>', expressions.sum_4days, name='sum4days'),
]