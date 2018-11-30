from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import datetime
from django.utils import timezone
import math
import os

time_step = [datetime.timedelta(0, 5), 
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

max_box = 10
min_box = 0
big_step = 6
small_step = 1

def get_level (data_bases, user):
	'''	Acquisition of the user level
		@param data_bases Databases for a specific language
		@param user Current platform user
		@return Current level from this user
	'''
	relationship = data_bases['user'].latest_relationship(user)

	if relationship.time <= timezone.now():
		level = relationship.number
	else:
		level = next_level(data_bases, user)
		amount_total = get_amount_total (data_bases)

		if level > amount_total:
			level = relationship.number
		else:
			data_bases['user'].create(user, yesterday(), level)

	return level

def get_amount_total (data_bases):
	'''	Acquisition of the total number of records
		in the database
		@param data_bases Database under analysis
		@return The total amount, if any database,
		otherwise 300 
	'''
	if data_bases['specific']:
		return data_bases['specific'].amount_total()
	else:
		return 300

def get_url_video (sentence):
	'''	Acquire the video URL
		@param sentence Video's characteristic sentence
		@return The video URL
	'''
	url_video = 'http://localhost:8000/static/video/' + sentence + '.mp4'

	print ("URL: " + str(url_video))

	return url_video

def get_current_box (data_bases, user, level):
	'''	Acquisition of the current context of the user
		@param data_bases Databases for a specific language
		@param user Current platform user
		@param level Current level from user
		@return Current context
	'''
	current_box = data_bases['user'].find(user, level).box

	print("Current box: " + str(current_box))

	return current_box

def next_level (data_bases, user):
	'''	Add a level to the user
		@param data_bases Databases for a specific language
		@param user Current platform user
		@return Correct next level
	'''
	return data_bases['user'].get_level(user) + 1

def easy_common (data_bases, user_data):
	'''	Common rule for the choice of low difficulty
		@param data_bases Databases for a specific language
		@param user Current platform user
		@return User registration update
	'''

	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship = db.find(user, next_level)

	if current_box != max_box:
		if current_box == min_box:
			step = big_step
		else:
			step = small_step

		current_box = current_box + step
		
		relationship.box = current_box

	relationship.time = update_time (current_box)
	relationship.save()

	return

def medium_common (data_bases, user_data):
	'''	Common rule for the choice of medium difficulty
		@param data_bases Databases for a specific language
		@param user Current platform user
		@return User registration update
	'''
	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship =  db.find(user, next_level)
	relationship.time = update_time(current_box)
	relationship.save()

	return

def hard_common (data_bases, user_data):
	'''	Common rule for the choice of hard difficulty
		@param data_bases Databases for a specific language
		@param user Current platform user
		@return User registration update
	'''
	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship =  db.find(user, next_level)

	if current_box > min_box:
		current_box = current_box - small_step
		relationship.box = current_box

	relationship.time = update_time(current_box)
	relationship.save()

	return

def yesterday():
	'''	Acquisition of yesterday, correctly
	'''
	return datetime.datetime.now() - datetime.timedelta(days = 1)

def update_time(current_box):
	'''	Acquisition of next sentence test time
		@param current_box Current context 
	'''
	return timezone.now() + time_step[current_box]

