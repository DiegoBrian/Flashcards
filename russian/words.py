from myproject.settings import BASE_DIR
from bs4 import BeautifulSoup
from russian.models import *
from language.views_common import *
import requests

##	@var words_step
#	Amount of words per page in the database
words_step = 50


@login_required
def index (request):
	data_bases = {
		'user': User_Word
	}

	level = get_level (data_bases, request.user)

	print(level)
	
	scraping = get_scraping (level)
	
	current_box = get_current_box (data_bases, request.user, level)

	context = {
		'title': "Russian",
		'soup' : scraping,
		'current_box' : current_box
	}
		
	return render(request, 'russian/words.html',context)

##	Acquisition of data on the word of the current level
#	@param level Current user level
#	@return Number, audio, cyrillic, english and function
#	about this word
def get_scraping (level):
	file_path = get_file_path (level)

	columns = get_columns (file_path, level)

	return get_scraping2 (level, columns)

##	Acquire the file path
#	@param level Current user level
#	@return The file path 
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

##	Characterization of data columns for the current level
#	@param file_path The source file path
#	@param level Current user level
#	@return Matching columns
def get_columns (file_path, level):
	if level <= max_amount:
		soup = BeautifulSoup (open (file_path, encoding='utf-8'), "html.parser")	
		
		table = soup.find ("table", attrs = {'class': 'topwords'})
		
		columns = table.find_all("td")

		return columns

##	Acquisition of data on the word of the current level
#	and known columns
#	@param level Current user level
#	@param columns Matching columns
#	@return Number, audio, cyrillic, english and function
#	about this word
def get_scraping2 (level, columns):
	if level <= words_step :
		factor = 5

	elif level <= words_step * 6:
		factor = 4

	return get_data (level, columns[factor:])

##	Acquisition of data relating to a word
#	@param level Current user level
#	@param columns Matching columns
#	@return Number, audio, cyrillic, english and function
#	about this word
def get_data (level, columns):
	sync = get_sync(level)

	data = {
		'number': filter_cyrillic (columns[sync].text),
		'audio': get_pronunciation_path (filter_cyrillic (columns[sync + 2].text)),
		'cyrillic': filter_cyrillic (columns[sync + 2].text),
		'english': columns[sync + 3].text,
		'function': columns[sync + 4].text
	}
	
	return data

##	Synchronization of colums for data acquisition
#	@param level Current user level
#	@return 
def get_sync (level):
	if level  <= words_step :
		sync = 5 * (level - 1)
	else:
		if level <= words_step * 5:
			weight = words_step
		else:
			weight = words_step * 2
		
		sync = 4 * (level - (weight * (math.ceil (level/weight) - 1) + 1))

		sync = sync - 1

	return sync

def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

##	Acquiring the path of the pronunciation file
#	@param word Word under analysis
#	@return The path of the pronunciation file
def get_pronunciation_path (word):
	file_path = 'http://localhost:8000/static/audio/words/'+word.replace(" ","_")+'.mp3'
	return file_path

##	Cyrillic characters for acceptable characters
#	@param word Word under analysis
#	@return Word with acceptable characters
def filter_cyrillic (word):
	return word.replace(u'\xa0', u'')

##	Rule for the choice of low difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
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

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
@login_required
def ok (request, number, current_box):
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

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
@login_required
def hard (request, number, current_box):
	data_bases = {
		'user': User_Word
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	hard_common (data_bases, user_data)

	return redirect('words')
