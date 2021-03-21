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
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'update accounts_user set dark_mode = ' + str(Dark) + ' where id = ' + str(user.id)
	cursor.execute(query)
	conn.commit()
	form = settingForm()
	return render(request, 'settings.html', {'form' : form})

