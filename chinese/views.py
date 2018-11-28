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

'''
verificar controls
verificar lógica dos botões Hard, Good e Easy
'''

@login_required
def index (request):
	level = controller (request.user)

	print("Level: " + str(level))

	sentence = Sentence.find(level)

	current = User_Sentence.find(request.user, level)

	video = get_video_url(sentence.sentence)

	context = {
		'title': "Chinese",
		'sentence' : sentence,
		'current_box' : current.box,
		'video' : video
	}

	return render(request, 'index.html', context)

def get_video_url(sentence):
	print("Vídeo: " + sentence)
	return 'http://localhost:8000/static/video/' + sentence + '.mp4'

def controller (user):
	relationship = User_Sentence.relationship(user)

	if not relationship:
		User_Sentence.create(user, yesterday())

	relationship = User_Sentence.relationship(user).order_by('time').first()

	if relationship.time <= timezone.now():
		level = relationship.sentence_number
	else:
		level = get_level(user) + 1
		number_of_words = Sentence.number_of_words()
		if(level > number_of_words):
			level = relationship.sentence_number
		else:
			User_Sentence.create(user, yesterday(), level)
	
	return level

def get_level (user):
	relationship = User_Sentence.relationship(user).order_by('-sentence_number').first()
	return relationship.sentence_number

@login_required
def easy (request, sentence_number, current_box):
	relationship =  User_Sentence.find(request.user, sentence_number)

	if current_box != 10:
		if current_box == 0:
			step = 6
		else:
			step = 1
		
		current_box = current_box + step
		
		relationship.box = current_box

	relationship.time = update_time(current_box)
	relationship.save()

	return redirect('chinese_index')

@login_required
def ok (request, sentence_number, current_box):
	relationship =  User_Sentence.find(request.user, sentence_number)

	relationship.time = update_time(current_box)

	relationship.save()

	return redirect('chinese_index')


@login_required
def hard (request, sentence_number, current_box):
	relationship =  User_Sentence.find(request.user, sentence_number)

	if current_box != 0:
		current_box = current_box - 1
		relationship.box = current_box

	relationship.time = update_time(current_box)
	relationship.save()

	return redirect('chinese_index')

def yesterday():
	return datetime.datetime.now() - datetime.timedelta(days = 1)

def update_time(current_box):
	return timezone.now() + time[current_box]