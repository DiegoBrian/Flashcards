from myproject.settings import BASE_DIR
from bs4 import BeautifulSoup
from russian.models import *
from language.views import *
import requests

words_step = 50


@login_required
def index (request):
	'''
	'''
	data_bases = {
		'user': User_Word
	}

	level = get_level (data_bases, request.user)

	print(level)
	
	scraping = get_scraping (level)
	
	current_box = get_current_box (request.user, level)

	context = {
		'title': "Russian",
		'soup' : scraping,
		'current_box' : current_box
	}
		
	return render(request, 'russian/words.html',context)

def get_scraping (level):
	file_path = get_file_path (level)

	columns = get_columns (file_path, level)

	return get_scraping (level, columns)

def get_file_path (level):
	if level <= words_step:
		specific_path = ""

	elif level <= words_step * 5:
		specific_path = str(math.ceil (level / words_step ))

	elif level <= words_step * 6:
		specific_path = str(math.ceil (level/ (words_step * 2) ) + 2)

	file_path = os.path.join (	BASE_DIR,
								'russian\static\html\\Most Common Russian Words' 
								+ specific_path
								+ '.html')

	return file_path

def get_columns (file_path, level):
	if level <= max_amount:
		soup = BeautifulSoup (open (file_path, encoding='utf-8'), "html.parser")	
		
		table = soup.find ("table", attrs = {'class': 'topwords'})
		
		columns = table.find_all("td")

		return columns

def get_scraping (level, columns):
	if level <= words_step :
		factor = 5

	elif level <= words_step * 6:
		factor = 4

	return get_data (level, columns[factor:])

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	file_path = 'http://localhost:8000/static/audio/words/'+query.replace(" ","_")+'.mp3'
	return file_path

def filter_cyrillic(word):
	return word.replace(u'\xa0', u'')

@login_required
def easy (request, number, current_box):
	data_bases = {
		'user': User_Word
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	easy_common (data_bases, user_data)

	return redirect('words')


@login_required
def ok (request, word_number, current_box):
	data_bases = {
		'user': User_Word
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	medium_common (data_bases, user_data)

	return redirect('words')


@login_required
def hard (request, word_number, current_box):
	ata_bases = {
		'user': User_Word
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	hard_common (data_bases, user_data)

	return redirect('words')


def get_data (level, columns):
	counter = get_counter(level)

	scraping = {
		'number': filter_cyrillic (columns[counter].text),
		'audio': get_pronunciation (filter_cyrillic (columns[counter + 2].text)),
		'cyrillic': filter_cyrillic (columns[counter + 2].text),
		'english': columns[counter + 3].text,
		'function': columns[counter + 4].text
	}
	
	return scraping

def get_counter (level):
	if level  <= words_step :
		counter = 5 * (level - 1)
	else:
		if level <= words_step * 5:
			weight = words_step
		else:
			weight = words_step * 2
		
		counter = 4 * (level - (weight * (math.ceil (level/weight) - 1) + 1))

		counter = counter - 1

	return counter