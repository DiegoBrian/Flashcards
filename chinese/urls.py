from django.urls import path

from chinese import views

urlpatterns = [
	path('', views.index, name = 'chinese_index'),
	path('shard/<int:number>/<int:current_box>/', views.hard, name='sentence_hard'),
    path('sok/<int:number>/<int:current_box>/', views.ok, name='sentence_ok'),
    path('seasy/<int:number>/<int:current_box>/', views.easy, name='sentence_easy'),
]