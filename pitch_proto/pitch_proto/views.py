from django.shortcuts import render
import psycopg2
import pandas as pd
import recommendationTest.views

def getPopular():
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'select track_id from recommender_track where track_popularity > 80 order by random() limit 9'
	cursor.execute(query)
	hold = cursor.fetchall()
	x = 8
	cleanids = []
	while(x >= 0):
		cleanids.append(hold[x][0])
		x = x - 1
	return cleanids
def homepage(request):
	"""
	This displays the landing/login page if user is not authenticated. It
	displays the logged in homepage if they are.
	"""
	popids = getPopular()
	if request.user.is_authenticated:
		recommendationTest.views.tableEntry(request.user.id)
		songids = recommendationTest.views.grabQuickRec(request.user.id)
		return render(request, 'home.html', {'songids' : songids[0][0], 'popids' : popids})
	return render(request, 'home.html', {'popids' : popids})
