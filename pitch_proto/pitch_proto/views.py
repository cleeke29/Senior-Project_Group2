from django.shortcuts import render
import psycopg2
import pandas as pd
import recommendationTest.views

def homepage(request):
	if request.user.is_authenticated:
		recommendationTest.views.tableEntry(request.user.id)
		dance = recommendationTest.views.getRecs('danceability', request.user.id)
		dance2 = recommendationTest.views.getRecs('danceability', request.user.id)
		acoustic = recommendationTest.views.getRecs('acousticness', request.user.id)
		acoustic2 = recommendationTest.views.getRecs('acousticness', request.user.id)
		tempo = recommendationTest.views.getRecs('tempo', request.user.id)
		tempo2 = recommendationTest.views.getRecs('tempo', request.user.id)
		return render(request, 'home.html', {'dance' : dance, 'acoustic' : acoustic, 'tempo' : tempo, 'dance2' : dance2, 'acoustic2' : acoustic2, 'tempo2' : tempo2})
	return render(request, 'home.html')
