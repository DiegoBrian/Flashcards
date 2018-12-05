from language.views_common import *
from russian.models import *
import requests

##	@var words_step
#	Amount of words per page in the database
expressions_max = 100

@login_required
def index (request):
	data_bases = {
		'user': User_Expression
	}

	level = get_level (data_bases, request.user)

	scraping = get_scraping (level)

	current_box = get_current_box (data_bases, request.user, level)

	context = {
		'title': "Russian",
		'soup' : scraping,
		'current_box' : current_box
	}

	return render(request, 'russian/expressions.html', context)

##	Acquisition of data on the word of the current level
#	@param level Current user level
#	@return Number, audio, cyrillic, english and function
#	about this word
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


def get_soup(url, header):
	r = requests.get(url, headers=header, allow_redirects=True)
	return BeautifulSoup(r.content, 'html.parser')

def get_pronunciation(query):
	file_path = 'http://localhost:8000/static/audio/expressions/' +query[10:]
	return file_path

def filter_cyrillic(word):
	return word.replace(u'\xa0', u'').replace('\n', '')



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
