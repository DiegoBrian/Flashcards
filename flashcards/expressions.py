from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup
from flashcards.models import *
import datetime
from django.utils import timezone
import math

@login_required
def index (request):

	level = controller (request.user)

	print(level)

	url = 'http://www.nemoapps.com/phrasebooks/russian'

	
	header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"}
	soup = get_soup(url,header)
	columns = soup.find_all("td")
	scraping = []
		
	scraping = get_data(level, columns)

	return render(request, 'expressions.html',{'soup' : scraping})

def winner(request):
	pass

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	return 'http://www.nemoapps.com' + query

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
		User_Expression.objects.create(user = user, expression_number = level, time = datetime.datetime.now() - datetime.timedelta(days=1))
		
	
	return level
	

def get_level (user):
	relationship = User_Expression.objects.filter(user = user).order_by('-expression_number')
	return relationship[0].expression_number

@login_required
def sum_1min (request, expression_number):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=1)
	relationship.save()
	return redirect('expressions')

@login_required
def sum_10min (request, expression_number):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=10)
	relationship.save()
	return redirect('expressions')

@login_required
def sum_4days (request, expression_number):
	relationship =  User_Expression.objects.get(user = request.user, expression_number=expression_number)
	relationship.time = timezone.now() + datetime.timedelta(days=4)
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
