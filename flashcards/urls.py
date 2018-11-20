from django.urls import path

from . import words
from . import expressions
from . import index
from . import teste

urlpatterns = [
	path('', index.index, name = 'index'),
    path('words', words.index, name='words'),
    path('whard/<int:word_number>/<int:current_box>/', words.hard, name='word_hard'),
    path('wok/<int:word_number>/<int:current_box>/', words.ok, name='word_ok'),
    path('weasy/<int:word_number>/<int:current_box>/', words.easy, name='word_easy'),
    path('expressions', expressions.index, name='expressions'),
    path('ehard/<int:expression_number>/<int:current_box>/', expressions.hard, name='expression_hard'),
    path('eok/<int:expression_number>/<int:current_box>/', expressions.ok, name='expression_ok'),
    path('eeasy/<int:expression_number>/<int:current_box>/', expressions.easy, name='expression_easy'),

	path('testes/', teste.teste, name='teste'),    
]