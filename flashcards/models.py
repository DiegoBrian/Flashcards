from django.db import models
from django.conf import settings

class Word(models.Model):
	number = models.CharField('Number', max_length=10)
	word = models.CharField('Word', max_length=256)
	pronunciation = models.CharField('Pronunciation', max_length=256)
	equivalence = models.CharField('Equivalence', max_length=256)
	part_of_speech = models.CharField('Part of speech', max_length = 256, null=True, blank=True)
	image = models.ImageField(upload_to='images', verbose_name='Image', null=True, blank=True)



class User_Word(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
	word_number = models.IntegerField('Word Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)


class User_Expression(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
	expression_number = models.IntegerField('Expression Number')
	time = models.DateTimeField('Time')
	box = models.IntegerField('Box', default=0)
