from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from chinese.models import *
from language.views_common import *
import datetime
import json

def choose_language (request):
	return render(request, 'language/index.html')

def time(request):
	#print(get_time_step(request.user))

	if request.method == 'POST':
		t1n = request.POST['time1number']
		t1s = request.POST['time1select']
		t2n = request.POST['time2number']
		t2s = request.POST['time2select']
		t3n = request.POST['time3number']
		t3s = request.POST['time3select']
		t4n = request.POST['time4number']
		t4s = request.POST['time4select']
		t5n = request.POST['time5number']
		t5s = request.POST['time5select']
		t6n = request.POST['time6number']
		t6s = request.POST['time6select']
		t7n = request.POST['time7number']
		t7s = request.POST['time7select']
		t8n = request.POST['time8number']
		t8s = request.POST['time8select']
		t9n = request.POST['time9number']
		t9s = request.POST['time9select']
		t10n = request.POST['time10number']
		t10s = request.POST['time10select']
		t11n = request.POST['time11number']
		t11s = request.POST['time11select']

		time_step = [convert_delta(t1n,t1s),
		 			convert_delta(t2n,t2s),
		 			convert_delta(t3n,t3s),
		 			convert_delta(t4n,t4s),
		 			convert_delta(t5n,t5s),
		 			convert_delta(t6n,t6s),
		 			convert_delta(t7n,t7s),
		 			convert_delta(t8n,t8s),
		 			convert_delta(t9n,t9s),
		 			convert_delta(t10n,t10s),
		 			convert_delta(t11n,t11s)]

		set_time_step(request.user, time_step)
	
	context = {
		'times' : revert_delta(request.user)
	}
	
	return render(request, 'russian/time.html', context)
	

def convert_delta (time_number, time_select):
	if time_number:
		time_number = int(time_number)
		if time_select == 'seg':
			return datetime.timedelta(0,time_number)
		elif time_select == 'min':
			return datetime.timedelta(0,time_number*60)
		elif time_select == 'hour':
			return datetime.timedelta(0,time_number*3600)
		elif time_select == 'day':
			return datetime.timedelta(time_number)
		elif time_select == 'week':
			return datetime.timedelta(time_number*7)
		elif time_select == 'month':
			return datetime.timedelta(time_number*30)
		elif time_select == 'year':
			return datetime.timedelta(time_number*365)


def revert_delta (user):
	time_step = get_time_step(user)

	time_str = []

	for time in time_step:
		date = time.days*86400+time.seconds
		if date >= 31536000:
			years = date/86400/365
			years_str = str(years).rstrip('0').rstrip('.') 
			time_str.append(years_str + " year(s)")
		elif date >= 2592000:
			months = date/86400/30
			months_str = str(months).rstrip('0').rstrip('.')
			time_str.append(months_str +" month(s)")
		elif date >= 604800:
			weeks = date/86400/7
			weeks_str = str('%.1f' % weeks).rstrip('0').rstrip('.')
			time_str.append(weeks_str +" week(s)")
		elif date >= 86400:
			days = date/86400
			days_str = str(days).rstrip('0').rstrip('.')
			time_str.append(days_str +" day(s)")
		elif date >= 3600:
			hours = date/3600
			hours_str = str(hours).rstrip('0').rstrip('.')
			time_str.append(hours_str +" hour(s)")
		elif date >= 60:
			minutes = date/60
			minutes_str = str(minutes).rstrip('0').rstrip('.')
			time_str.append(minutes_str +" minute(s)")
		else:
			seconds = date
			seconds_str = str(seconds).rstrip('0').rstrip('.')
			time_str.append(seconds_str + " second(s)")

	return time_str