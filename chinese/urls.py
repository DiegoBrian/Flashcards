from django.urls import path

from chinese import views

urlpatterns = [
	path('', views.index, name = 'chinese_index'),
]