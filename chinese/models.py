from django.db import models
from django.conf import settings
from language.views_common import yesterday

class Sentence(models.Model):
	number = models.IntegerField('Number', default=0, blank= True, null=True)
	sentence = models.CharField('Sentence', max_length=3000)
	pinyin = models.CharField('Pinyin', max_length=3000, blank= True, null=True)
	equivalence = models.CharField('Equivalence in English', max_length=3000, blank= True, null=True)

	def __str__ (self):
		return '('+str(self.number)+')'+self.sentence

	def find (number):
		return Sentence.objects.get(number = number)

	def get_sentence (number):
		return Sentence.find(number).sentence

	def amount_total ():
		return Sentence.objects.all().count()

class User_Sentence(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	number = models.IntegerField('Sentence Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)

	def create (user, time, number = 1):
		User_Sentence.objects.create(user = user,
									number = number,
									time = time)

	def find (user):
		return User_Sentence.objects.get(user = user)

	def find (user, level):
		return User_Sentence.objects.get(user = user,
										number = level)

	def relationship (user):
		return User_Sentence.objects.filter(user = user)

	def latest_relationship (user):
		relationship = User_Sentence.relationship(user)

		if not relationship:
			User_Sentence.create(user, yesterday())

		relationship = User_Sentence.relationship(user).order_by('time').first()

		return relationship

	def get_level (user):
		relationship = User_Sentence.relationship(user).order_by('-number').first()
		return relationship.number