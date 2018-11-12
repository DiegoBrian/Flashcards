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

	if level<=100:	
		file_path = os.path.join(BASE_DIR, 'flashcards\static\html\\100 Russian Phrases with Audio.html')
		soup = BeautifulSoup(open(file_path, encoding='utf-8'), "html.parser")	
		columns = soup.find_all("td")
	scraping = []
	
	if level<=100:	
		scraping = get_data(level, columns)

	current_box = get_current_box(request.user, level)

	context = {
		'soup' : scraping,
		'current_box' : current_box
		}

	return render(request, 'expressions.html',context)

def get_current_box(user, expression_number):
	expression = User_Expression.objects.get(user = user, expression_number=expression_number)
	return expression.box

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	file_path = 'http://localhost:8000/static/audio/expressions/' +query[10:]
	return file_path

def filter_cyrillic(word):
	return word.replace(u'\xa0', u'').replace('\n', '')


def controller (user):
	relationship = User_Expression.objects.filter(user = user)
	if not relationship:
		User_Expression.objects.create(user = user, expression_number = 1, time = datetime.datetime.now() - datetime.timedelta(days=1))

	relationship = User_Expression.objects.filter(user = user).order_by('time')

	if relationship[0].time <= timezone.now():
		level = relationship[0].expression_number
	else:
		level = get_level(user)+1
		if level <=100:
			User_Expression.objects.create(user = user, expression_number = level, time = datetime.datetime.now() - datetime.timedelta(days=1))
		else:
			level = relationship[0].expression_number				
		
	
	return level

def delete_all(user):
	teste = User_Expression.objects.filter(user=user).delete()
	

def get_level (user):
	relationship = User_Expression.objects.filter(user = user).order_by('-expression_number')
	return relationship[0].expression_number

@login_required
def easy (request, expression_number, current_box):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
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
	return redirect('expressions')


@login_required
def ok (request, expression_number, current_box):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
	print(relationship.time)
	relationship.time = timezone.now() + time[current_box]
	print(relationship.time)
	relationship.save()
	return redirect('expressions')


@login_required
def hard (request, expression_number, current_box):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
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
	return redirect('expressions')


def get_data (level, columns):
	scraping = []
	counter = 2*level-1
	line = []
	line.append(str(level)+'.')
	expression = columns[counter].find_all("strong")
	line.append(expression[0].text)
	line.append(expression[1].text)
	line.append(columns[counter].find("div", attrs={'class': 'translation'}).text)
	line.append(get_pronunciation(columns[counter-1].find("source").get('src')))
	scraping.append(line)

	return scraping
