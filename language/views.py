from django.shortcuts import render, redirect

def choose_language (request):
	return render(request, 'language/index.html')