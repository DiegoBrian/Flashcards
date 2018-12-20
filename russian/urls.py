from django.urls import path

from russian import words, expressions, index

urlpatterns = [
    path('', index.index, name='index'),
    path('words', words.index, name='words'),
    path('whard/<int:number>/<int:current_box>/', words.hard, name='word_hard'),
    path('wok/<int:number>/<int:current_box>/', words.ok, name='word_ok'),
    path('weasy/<int:number>/<int:current_box>/', words.easy, name='word_easy'),

    path('expressions', expressions.index, name='expressions'),
    path('ehard/<int:number>/<int:current_box>/',
         expressions.hard, name='expression_hard'),
    path('eok/<int:number>/<int:current_box>/',
         expressions.ok, name='expression_ok'),
    path('eeasy/<int:number>/<int:current_box>/',
         expressions.easy, name='expression_easy'),
]
