from django.db import models
from django.conf import settings

class Sentence(models.Model):
	number = models.IntegerField('Number', default=0)
	sentence = models.CharField('Sentence', max_length=3000)
	pinyin = models.CharField('Pinyin', max_length=3000)
	equivalence = models.CharField('Equivalence in English', max_length=3000)
	

class User_Sentence(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	sentence_number = models.IntegerField('Sentence Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)
