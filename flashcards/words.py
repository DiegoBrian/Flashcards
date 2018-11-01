from django.shortcuts import render, redirect
import requests
from bs4 import BeautifulSoup
from flashcards.models import *
import datetime
from django.utils import timezone
import math

def index (request):

	level = controller (request.user)

	print(level)

	if level <= 50 :
		url = 'http://masterrussian.com/vocabulary/most_common_words.htm'
	else:
		url = 'http://masterrussian.com/vocabulary/most_common_words_'+str(math.ceil(level/50))+'.htm'

	
	header = {'User-Agent': "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; Touch; rv:11.0) like Gecko"}
	soup = get_soup(url,header)
	table = soup.find("table", attrs={'class': 'topwords'})
	columns = table.find_all("td")
	scraping = []
	
	if level <= 50 :
		scraping = get_data(level, columns[5:])
	else:
		scraping = get_data2(level, columns[4:])
	
		
	return render(request, 'index.html',{'soup' : scraping})

def winner(request):
	pass

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	return 'https://openrussian.org/audio-shtooka/' + query.replace(" ","_") + '.mp3'

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
	

def get_level (user):
	relationship = User_Word.objects.filter(user = user).order_by('-word_number')
	return relationship[0].word_number


def sum_1min (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=1)
	relationship.save()
	return redirect('index')

def sum_10min (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(minutes=10)
	relationship.save()
	return redirect('index')

def sum_4days (request, word_number):
	relationship =  User_Word.objects.get(user = request.user, word_number=word_number)
	relationship.time = timezone.now() + datetime.timedelta(days=4)
	relationship.save()
	return redirect('index')


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
	counter = 4*(level-50*(math.ceil(level/50))-1)
	
	line = []
	line.append(filter_cyrillic(columns[counter].text))
	line.append(get_pronunciation(filter_cyrillic(columns[counter+1].text)))
	line.append(filter_cyrillic(columns[counter+1].text))
	line.append(columns[counter+2].text)
	line.append(columns[counter+3].text)
	scraping.append(line)

	return scraping