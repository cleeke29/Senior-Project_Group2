from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd
import recommendationTest.views


def settingsPage(request):
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})
#allows user to change user name if it is not blank
def changeUsername(request):
	user = request.user
	form = settingForm(request.POST)
	if form.is_valid():
		username = form.cleaned_data['newUser']
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	if username is not '':
		query = "update accounts_user set username = '" + username + "' where id = " + str(user.id)
		cursor.execute(query)
		conn.commit()
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})
#will toggle on or off dark mode
def toggleDark(request):
	user = request.user
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'select dark_mode from accounts_user where id = ' + str(user.id)
	cursor.execute(query)
	toggle = cursor.fetchone()[0]
	if (toggle):
		query = 'update accounts_user set dark_mode = false where id = ' + str(user.id)
	else:
		query = 'update accounts_user set dark_mode = true where id = ' + str(user.id)
	cursor.execute(query)
	conn.commit()
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})
#will reset the prefferences, this will put your preffered back to the averages.
def settingsReset(request):
	form = settingForm()
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'update "recommendationTest_preferredmusic" set "danceabilityPreferred" = 0.5175604065506179, "acousticnessPreferred" = 0.5124401243104162, "tempoPreferred" = 116.89153340585992, "energyPreferred" = 0.4912925703706923, "instrumentalnessPreferred" = 0.2182890461397754, "livenessPreferred" = 0.22849001657009402, "loudnessPreferred" = -11.807307819952968, "speechinessPreferred" = 0.08092244415462105, "valencePreferred" = 0.49786766966548757 where id = ' + str(request.user.id)
	cursor.execute(query)
	conn.commit()
	id = request.user.id
	songids = []
	songids.append(recommendationTest.views.getRecs('danceability', id))
	songids.append(recommendationTest.views.getRecs('acousticness', id))
	songids.append(recommendationTest.views.getRecs('tempo', id))
	songids.append(recommendationTest.views.getRecs('energy', id))
	songids.append(recommendationTest.views.getRecs('loudness', id))
	songids.append(recommendationTest.views.getRecs('speechiness', id))
	songids.append(recommendationTest.views.getRecs('instrumentalness', id))
	songids.append(recommendationTest.views.getRecs('liveness', id))
	songids.append(recommendationTest.views.getRecs('valence', id))
	recommendationTest.views.buildQuickRec(id, songids)
	return render(request, 'settings.html', {'form' : form})



