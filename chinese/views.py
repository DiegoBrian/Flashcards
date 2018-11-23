from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from chinese.models import *
from django.utils import timezone
import math
import os

time = [datetime.timedelta(0, 5), 
		datetime.timedelta(0, 25), 
		datetime.timedelta(0, 120), 
		datetime.timedelta(0, 600), 
		datetime.timedelta(0, 3600), 
		datetime.timedelta(0, 18000), 
		datetime.timedelta(1), 
		datetime.timedelta(5), 
		datetime.timedelta(25),
		datetime.timedelta(120),
		datetime.timedelta(365)]

@login_required
def index (request):
	level = controller (request.user)

	print(level)

	sentence = Sentence.objects.get(number = level)

	current = User_Sentence.objects.get(user = request.user, sentence_number = level)

	context = {
		'sentence' : sentence,
		'current_box' : current.box
	}

	return render(request, 'index.html', context)

def controller (user):
	relationship = User_Sentence.objects.filter(user = user)
	if not relationship:
		User_Sentence.objects.create(user = user, sentence_number = 1, time = datetime.datetime.now() - datetime.timedelta(days=1))

	relationship = User_Sentence.objects.filter(user = user).order_by('time')

	if relationship[0].time <= timezone.now():
		level = relationship[0].sentence_number
	else:
		level = get_level(user)+1
		number_of_words = Sentence.objects.all().count()
		if(level > number_of_words):
			level = relationship[0].sentence_number	
		else:
			User_Sentence.objects.create(user = user, sentence_number = level, time = datetime.datetime.now() - datetime.timedelta(days=1))
		
	return level


def get_level (user):
	relationship = User_Sentence.objects.filter(user = user).order_by('-sentence_number')
	return relationship[0].sentence_number


@login_required
def easy (request, sentence_number, current_box):
	relationship =  User_Sentence.objects.get(user = request.user, sentence_number=sentence_number)
	print(relationship.time)
	if current_box == 10:
		relationship.time = timezone.now() + time[current_box]
	else:
		new_box = current_box+1
		relationship.time = timezone.now() + time[new_box]
		print("new_box: "+str(new_box))
		relationship.box = new_box
		relationship.save()
	print(relationship.time)
	relationship.save()
	return redirect('chinese_index')


@login_required
def ok (request, sentence_number, current_box):
	relationship =  User_Sentence.objects.get(user = request.user, sentence_number=sentence_number)
	print(relationship.time)
	relationship.time = timezone.now() + time[current_box]
	print(relationship.time)
	relationship.save()
	return redirect('chinese_index')


@login_required
def hard (request, sentence_number, current_box):
	relationship =  User_Sentence.objects.get(user = request.user, sentence_number=sentence_number)
	print(relationship.time)
	if current_box == 0:
		relationship.time = timezone.now() + time[current_box]
	else:
		new_box = current_box-1
		relationship.time = timezone.now() + time[new_box]
		relationship.box = new_box
		relationship.save()
	print(relationship.time)
	relationship.save()
	return redirect('chinese_index')