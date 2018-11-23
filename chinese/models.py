from django.db import models
from django.conf import settings

class Sentence(models.Model):
	number = models.IntegerField('Number', default=0, blank= True, null=True)
	sentence = models.CharField('Sentence', max_length=3000)
	pinyin = models.CharField('Pinyin', max_length=3000, blank= True, null=True)
	equivalence = models.CharField('Equivalence in English', max_length=3000, blank= True, null=True)

	def __str__(self):
		return '('+str(self.number)+')'+self.sentence
	

class User_Sentence(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	sentence_number = models.IntegerField('Sentence Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)
