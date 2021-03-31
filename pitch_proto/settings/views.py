from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd

def settingsPage(request):
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})

def settingsUpdate(request):
	user = request.user
	form = settingForm(request.POST)
	if form.is_valid():
		Dark = form.cleaned_data['DarkMode']
		Explicit = form.cleaned_data['Explicit']
		username = form.cleaned_data['newUser']
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'update accounts_user set dark_mode = ' + str(Dark) + ', explicit = '+ str(Explicit) + ' where id = ' + str(user.id)
	cursor.execute(query)
	if username is not '':
		query = "update accounts_user set username = '" + username + "' where id = " + str(user.id)
		cursor.execute(query)
	conn.commit()
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})

def settingsReset(request):
	print('in')
	form = settingForm()
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'update "recommendationTest_preferredmusic" set "danceabilityPreferred" = 0.5175604065506179, "acousticnessPreferred" = 0.5124401243104162, "tempoPreferred" = 116.89153340585992 where id = ' + str(request.user.id)
	cursor.execute(query)
	conn.commit()
	return render(request, 'settings.html', {'form' : form})
