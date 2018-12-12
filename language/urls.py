from django.urls import path
from language import views

urlpatterns = [
    path('', views.choose_language, name = 'choose_language'),
    path('time/', views.time, name = 'time'),
]