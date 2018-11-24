from django.db import models
from django.conf import settings

class Sentence(models.Model):
	number = models.IntegerField('Number', default=0, blank= True, null=True)
	sentence = models.CharField('Sentence', max_length=3000)
	pinyin = models.CharField('Pinyin', max_length=3000, blank= True, null=True)
	equivalence = models.CharField('Equivalence in English', max_length=3000, blank= True, null=True)

	def __str__ (self):
		return '('+str(self.number)+')'+self.sentence

	def find (number):
		return Sentence.objects.get(number = number)

	def number_of_words ():
		return Sentence.objects.all().count()

class User_Sentence(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	sentence_number = models.IntegerField('Sentence Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)

	def find (user):
		return User_Sentence.objects.get(user = user)

	def find (user, level):
		return User_Sentence.objects.get(user = user,
										sentence_number = level)

	def relationship (user):
		return User_Sentence.objects.filter(user = user)

	def create (user, time):
		User_Sentence.objects.create(user = user,
									sentence_number = 1,
									time = time)
	
	def create (user, time, sentence_number):
		User_Sentence.objects.create(user = user,
									sentence_number = sentence_number,
									time = time)