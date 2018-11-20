from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from russian.models import *


def teste(request):

	Word.objects.create(number = 1, word= u'简体中文', pronunciation = 'pronunciation', equivalence='equivalence')
	
	words = Word.objects.all()

	context = {
		'words': words
	}

	return render(request, 'teste.html', context)
	


