from language.views_common import * 
from chinese.models import *


@login_required
def index (request):
	data_bases = {
		'user': User_Sentence,
		'specific': Sentence
	}

	level = get_level (data_bases, request.user)

	#print("Level: " + str(level))

	sentence = Sentence.find (level)

	current_box = get_current_box (data_bases, request.user, level)

	video = get_url_video (sentence.sentence)

	next_levels = get_next_levels(current_box)

	context = {
		'title': "Chinese",
		'sentence' : sentence,
		'current_box' : current_box,
		'video' : video,
		'next_levels': next_levels
	}

	return render(request, 'index.html', context)

##	Acquire the video URL
#	@param sentence Video's characteristic sentence, in chinese
#	@return The video URL
def get_url_video (sentence):
	url_video = 'http://localhost:8000/static/video/' + sentence + '.mp4'

	#print ("URL: " + str(url_video))

	return url_video

##	Rule for the choice of low difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
@login_required
def easy (request, number, current_box):
	data_bases = {
		'user': User_Sentence
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	easy_common (data_bases, user_data)

	return redirect('chinese_index')

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
@login_required
def ok (request, number, current_box):
	data_bases = {
		'user': User_Sentence
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	medium_common (data_bases, user_data)

	return redirect('chinese_index')

##	Rule for the choice of medium difficulty
#	@brief It demands user login
#	@param request Standard Django request
#	@param number Current user level
#	@param current_box	Current user context
#	@return Next page with a new word
@login_required
def hard (request, number, current_box):
	data_bases = {
		'user': User_Sentence
	}

	user_data = {
		'user': request.user,
		'next_level': number,
		'current_box': current_box
	}

	hard_common (data_bases, user_data)

	return redirect('chinese_index')