from language.views_common import *
from russian.models import *
import requests

##	@var expressions_max
#	Amount of expression per page in the database
expressions_max = 100

@login_required
def index (request):
	data_bases = {
		'user': User_Expression
	}

	level = get_level (data_bases, request.user)

	scraping = get_scraping (level)

	current_box = get_current_box (data_bases, request.user, level)

	next_levels = get_next_levels(current_box)

	context = {
		'title': "Russian",
		'soup' : scraping,
		'current_box' : current_box,
		'next_levels': next_levels
	}

	return render(request, 'russian/expressions.html', context)

##	Acquisition of data on the expression of the current level
#	@param level Current user level
#	@return Number, audio, expression, english and transliteration
#	about this expression
def get_scraping (level):
	if level <= expressions_max:
		file_path = get_file_path (level)

		columns = get_columns (file_path, level)

		return get_data (level, columns)

	return []

##	Acquire the file path
#	@param level Current user level
#	@return The file path 
def get_file_path (level):
	file_path = os.path.join(	BASE_DIR, 
								'russian\static\html\\100 Russian Phrases with Audio.html')

	return file_path

##	Characterization of data columns for the current level
#	@param file_path The source file path
#	@param level Current user level
#	@return Matching columns
def get_columns (file_path, level):
	soup = BeautifulSoup (open (file_path, encoding='utf-8'), "html.parser")
	
	columns = soup.find_all("td")

	return columns

##	Acquisition of data relating to a expression
#	@param level Current user level
#	@param columns Matching columns
#	@return Number, audio, expression, english and transliteration
#	about this expression
def get_data (level, columns):
	counter = (2 * level) - 1

	expression = columns[counter].find_all("strong")

	data = {
		'number': str(level) + '.',
		'expression': expression[0].text,
		'transliteration': expression[1].text,
		'english': columns[counter].find("div", attrs={'class': 'translation'}).text,
		'audio': get_pronunciation_path(columns[counter-1].find("source").get('src'))
	}

	return data


def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

##	Acquiring the path of the pronunciation file
#	@param query Expression under analysis
#	@return The path of the pronunciation file
def get_pronunciation_path(query):
	file_path = 'http://localhost:8000/static/audio/expressions/' + query[10:]
	return file_path

##	Rule for the choice of low difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new expression
@login_required
def easy (request, number, current_box):
	data_bases = {
		'user': User_Expression
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	easy_common (data_bases, user_data)

	return redirect('expressions')

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new expression
@login_required
def ok (request, number, current_box):
	data_bases = {
		'user': User_Expression
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	medium_common (data_bases, user_data)

	return redirect('expressions')

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new expression
@login_required
def hard (request, number, current_box):
	data_bases = {
		'user': User_Expression
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	hard_common (data_bases, user_data)

	return redirect('expressions')

