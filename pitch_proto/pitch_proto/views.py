from django.shortcuts import render
import psycopg2
import pandas as pd
import recommendationTest.views

def homepage(request):
	"""
	This displays the landing/login page if user is not authenticated. It
	displays the logged in homepage if they are.
	"""
	if request.user.is_authenticated:
		recommendationTest.views.tableEntry(request.user.id)
		songids = recommendationTest.views.grabQuickRec(request.user.id)
		return render(request, 'home.html', {'songids' : songids[0][0]})
	return render(request, 'home.html')
