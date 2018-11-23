from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from russian.models import *
import datetime
from django.utils import timezone
import math
import os
from myproject.settings import BASE_DIR

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

	if level <= 50 :
		file_path = os.path.join(BASE_DIR, 'russian\static\html\\Most Common Russian Words.html')
	elif level <= 250:
		file_path = os.path.join(BASE_DIR, 'russian\static\html\\Most Common Russian Words'+str(math.ceil(level/50))+'.html')
	elif level <= 300:
		file_path = os.path.join(BASE_DIR, 'russian\static\html\\Most Common Russian Words'+str(math.ceil(level/100)+2)+'.html')
	
	if level <= 300:
		soup = BeautifulSoup(open(file_path, encoding='utf-8'), "html.parser")	
		table = soup.find("table", attrs={'class': 'topwords'})
		columns = table.find_all("td")
		
	scraping = []
	
	if level <= 50 :
		scraping = get_data(level, columns[5:])
	elif level <= 300:
		scraping = get_data2(level, columns[4:])
	
	current_box = get_current_box(request.user, level)

	context = {
		'soup' : scraping,
		'current_box' : current_box
		}
		
	return render(request, 'russian/words.html',context)

def get_current_box(user, word_number):
	word = User_Word.objects.get(user = user, word_number=word_number)
	return word.box

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	file_path = 'http://localhost:8000/static/audio/words/'+query.replace(" ","_")+'.mp3'
	return file_path

def filter_cyrillic(word):
	return word.replace(u'\xa0', u'')


def controller (user):
	relationship = User_Word.objects.filter(user = user)
	if not relationship:
		User_Word.objects.create(user = user, word_number = 1, time = datetime.datetime.now() - datetime.timedelta(days=1))

	relationship = User_Word.objects.filter(user = user).order_by('time')

	if relationship[0].time <= timezone.now():
		level = relationship[0].word_number
	else:
		level = get_level(user)+1
		if level <=300:
			User_Word.objects.create(user = user, word_number = level, time = datetime.datetime.now() - datetime.timedelta(days=1))
		else:
			level = relationship[0].word_number		
		
	
	return level


def delete_all(user):
	teste = User_Word.objects.filter(user=user).delete()
	

def get_level (user):
	relationship = User_Word.objects.filter(user = user).order_by('-word_number')
	return relationship[0].word_number

@login_required
def easy (request, word_number, current_box):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
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
	return redirect('words')


@login_required
def ok (request, word_number, current_box):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	print(relationship.time)
	relationship.time = timezone.now() + time[current_box]
	print(relationship.time)
	relationship.save()
	return redirect('words')


@login_required
def hard (request, word_number, current_box):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
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
	return redirect('words')


def get_data (level, columns):
	counter = 5 * (level - 1)
	scraping = {
		'number': filter_cyrillic(columns[counter].text),
		'audio': get_pronunciation(filter_cyrillic(columns[counter+2].text)),
		'cyrillic': filter_cyrillic(columns[counter+2].text),
		'english': columns[counter+3].text,
		'function': columns[counter+4].text
	}
	
	return scraping

def get_data2 (level, columns):
	scraping = []
	if level<251:
		counter = 4*(level - (50*(math.ceil(level/50)-1)+1))
	else:
		counter = 4*(level - (100*(math.ceil(level/100)-1)+1))
	
	line = []
	line.append(filter_cyrillic(columns[counter].text))
	line.append(get_pronunciation(filter_cyrillic(columns[counter+1].text)))
	line.append(filter_cyrillic(columns[counter+1].text))
	line.append(columns[counter+2].text)
	line.append(columns[counter+3].text)
	scraping.append(line)

	return scraping