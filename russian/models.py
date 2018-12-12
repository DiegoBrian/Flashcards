from django.db import models
from django.conf import settings
from language.views_common import yesterday

class Word(models.Model):
	number = models.CharField('Number', max_length=10)
	word = models.CharField('Word', max_length=256)
	pronunciation = models.CharField('Pronunciation', max_length=256)
	equivalence = models.CharField('Equivalence', max_length=256)
	part_of_speech = models.CharField('Part of speech', max_length = 256, null=True, blank=True)
	image = models.ImageField(upload_to='images', verbose_name='Image', null=True, blank=True)

	def __str__ (self):
		return '(' + str(self.number) + ') ' + self.word

	def find (number):
		return Word.objects.get(number = number)


class User_Word(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
	number = models.IntegerField('Word Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)
	
	def create (user, time, number = 1):
		User_Word.objects.create(	user = user,
									number = number,
									time = time)

	def find (user):
		return User_Word.objects.get(user = user)

	def find (user, level):
		return User_Word.objects.get(user = user,
										number = level)

	def get_current_box(user, number):
		word = User_Word.find(user, number)
		return word.box

	def relationship (user):
		relationship = User_Word.objects.filter(user = user)
		return relationship

	def latest_relationship (user):
		relationship = User_Word.relationship(user)

		if not relationship:
			User_Word.create(user, yesterday())

		relationship = User_Word.relationship(user).order_by('time').first()

		return relationship

	def get_level (user):
		relationship = User_Word.relationship(user).order_by('-number').first()
		return relationship.number

	def delete_all(user):
		teste = User_Word.relationship(user).delete()


class User_Expression(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
	number = models.IntegerField('Expression Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)
	
	def create (user, time, number = 1):
		User_Expression.objects.create(	user = user,
									number = number,
									time = time)

	def find (user):
		return User_Expression.objects.get(user = user)

	def find (user, level):
		return User_Expression.objects.get(user = user,
										number = level)

	def get_current_box(user, number):
		word = User_Expression.find(user, number)
		return word.box

	def relationship (user):
		return User_Expression.objects.filter(user = user)

	def latest_relationship (user):
		relationship = User_Expression.relationship(user)

		if not relationship:
			User_Expression.create(user, yesterday())

		relationship = User_Expression.relationship(user).order_by('time').first()

		return relationship

	def get_level (user):
		relationship = User_Expression.relationship(user).order_by('-number').first()
		return relationship.number

	def delete_all(user):
		teste = User_Expression.relationship(user).delete()
