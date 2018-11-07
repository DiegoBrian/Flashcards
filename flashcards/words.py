from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from flashcards.models import *
import datetime
from django.utils import timezone
import math
import os
from russian_flashcards.settings import BASE_DIR

@login_required
def index (request):

	level = controller (request.user)

	print(level)

	if level == 301:
		delete_all(request.user)
		return redirect('words')

	if level <= 50 :
		file_path = os.path.join(BASE_DIR, 'flashcards\static\html\\Most Common Russian Words.html')
	elif level <= 250:
		file_path = os.path.join(BASE_DIR, 'flashcards\static\html\\Most Common Russian Words'+str(math.ceil(level/50))+'.html')
	else:
		file_path = os.path.join(BASE_DIR, 'flashcards\static\html\\Most Common Russian Words'+str(math.ceil(level/100)+2)+'.html')
	
	
	soup = BeautifulSoup(open(file_path, encoding='utf-8'), "html.parser")	
	table = soup.find("table", attrs={'class': 'topwords'})
	columns = table.find_all("td")
	scraping = []
	
	if level <= 50 :
		scraping = get_data(level, columns[5:])
	else:
		scraping = get_data2(level, columns[4:])
	
		
	return render(request, 'words.html',{'soup' : scraping})

def winner(request):
	pass

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
		User_Word.objects.create(user = user, word_number = level, time = datetime.datetime.now() - datetime.timedelta(days=1))
		
	
	return level


def delete_all(user):
	teste = User_Word.objects.filter(user=user).delete()
	

def get_level (user):
	relationship = User_Word.objects.filter(user = user).order_by('-word_number')
	return relationship[0].word_number

@login_required
def sum_1min (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=1)
	relationship.save()
	return redirect('words')

@login_required
def sum_10min (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=10)
	relationship.save()
	return redirect('words')

@login_required
def sum_12hours (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(hours=12)
	relationship.save()
	return redirect('words')


def get_data (level, columns):
	scraping = []
	counter = 5*(level-1)
	line = []
	line.append(filter_cyrillic(columns[counter].text))
	line.append(get_pronunciation(filter_cyrillic(columns[counter+2].text)))
	line.append(filter_cyrillic(columns[counter+2].text))
	line.append(columns[counter+3].text)
	line.append(columns[counter+4].text)
	scraping.append(line)

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