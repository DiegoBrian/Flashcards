##	@file Views_Common
#	Development of common rules, considering all handled languages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from myproject.settings import BASE_DIR
from django.utils import timezone
from bs4 import BeautifulSoup
import datetime
import math
import os

##	@var time_step
#	Standard time steps
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
##	@var max_amount 
#	Maximum capacity of snippets of languages, whether words, expressions or sentences
max_amount	= 300
##	@var max_box
#	Maximum possible time step
max_box		= 10
##	@var min_box
#	Minimum possible time step
min_box 	= 0
##	@var extr_step
#	Time step for extreme ease
extr_step 	= 6
##	@var std_step
#	Standard time step
std_step 	= 1

##	Acquisition of the user level
#	@param data_bases Databases for a specific language
#	@param user Current platform user
#	@return Current level from this user
def get_level (data_bases, user):
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

##	Acquisition of the total number of records
#	in the database
#	@param data_bases Database under analysis
#	@return The total amount, if any database,
#	otherwise max_amount 
def get_amount_total (data_bases):
	if hasattr(data_bases, 'specific'):
		return data_bases['specific'].amount_total()
	else:
		return max_amount

##	Acquisition of the current context of the user
#	@param data_bases Databases for a specific language
#	@param user Current platform user
#	@param level Current level from user
#	@return Current context
def get_current_box (data_bases, user, level):
	current_box = data_bases['user'].find(user, level).box

	print("Current box: " + str(current_box))

	return current_box

##	Add a level to the user
#	@param data_bases Databases for a specific language
#	@param user Current platform user
#	@return Correct next level
def next_level (data_bases, user):
	return data_bases['user'].get_level(user) + 1

##	Common rule for the choice of low difficulty
#	@param data_bases Databases for a specific language
#	@param user_data Current user data
#	@return User registration update
def easy_common (data_bases, user_data):
	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship = db.find(user, next_level)

	if current_box != max_box:
		if current_box == min_box:
			step = extr_step
		else:
			step = std_step

		current_box = current_box + step
		
		relationship.box = current_box

	relationship.time = update_time (current_box)
	relationship.save()

	return

##	Common rule for the choice of medium difficulty
#	@param data_bases Databases for a specific language
#	@param user_data Current user data
#	@return User registration update
def medium_common (data_bases, user_data):
	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship =  db.find(user, next_level)
	relationship.time = update_time(current_box)
	relationship.save()

	return

##	Common rule for the choice of hard difficulty
#	@param data_bases Databases for a specific language
#	@param user_data Current user data
#	@return User registration update
def hard_common (data_bases, user_data):
	db = data_bases['user']
	user = user_data['user']
	next_level = user_data['next_level']
	current_box = user_data['current_box']

	relationship =  db.find(user, next_level)

	if current_box > min_box:
		current_box = current_box - std_step
		relationship.box = current_box
	elif current_box < min_box:
		current_box = min_box

	relationship.time = update_time(current_box)
	relationship.save()

	return

##	Acquisition of yesterday, correctly
def yesterday():	
	return datetime.datetime.now() - datetime.timedelta(days = 1)

##	Acquisition of next sentence test time
#	@param current_box Current context 
#	@return Time updated
def update_time(current_box):
	return timezone.now() + time_step[current_box]

