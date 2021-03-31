from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd

connectionString = "host=localhost dbname=pitch_db user=admin password=admin"
def getAggregate(dataType):
	Aggregates = []
	# lowerbound, higher bound, avg, stddev
	if dataType == 'danceability':
		Aggregates.append(0.3323766490021055)
		Aggregates.append(0.7027441640991412)
		Aggregates.append(0.5175604065506179)
		Aggregates.append(0.18518375754852306)
		return Aggregates
	elif dataType == 'acousticness':
		Aggregates.append(0.14306341822142193)
		Aggregates.append(0.8818168303993985)
		Aggregates.append(0.5124401243104162)
		Aggregates.append(0.36937670608898837)
		return Aggregates
	elif dataType == 'tempo':
		Aggregates.append(85.77541351891276)
		Aggregates.append(148.0076532928066)
		Aggregates.append(116.89153340585992)
		Aggregates.append(31.116119886947722)
		return Aggregates
	# conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	# cursor = conn.cursor()
	# Aggregates = []
	# query = "select avg(" + dataType + ") - stddev(" + dataType + ") from recommender_audiofeatures"
	# cursor.execute(query)
	# Aggregates.append(cursor.fetchone()[0])
	# query = "select avg(" + dataType + ") + stddev(" + dataType + ") from recommender_audiofeatures"
	# cursor.execute(query)
	# Aggregates.append(cursor.fetchone()[0])
	# query = "select avg(" + dataType + ") from recommender_audiofeatures"
	# cursor.execute(query)
	# Aggregates.append(cursor.fetchone()[0])
	# # aggregates[0] = lower bound, aggregate[1] = higher bound, aggregate[2] = average
	# return Aggregates

def explicitCheck(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = "select explicit from recommender_track where track_id = '" + str(id) +"'"
	cursor.execute(query)
	return cursor.fetchone()[0]

def findSong(dataType, Aggregates, explicit):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	songids = []
	query = "select features_id from recommender_audiofeatures where " + dataType  + " < " + str(Aggregates[1]) + " and " + dataType + " > " + str(Aggregates[0]) +" order by random() limit 1"
	cursor.execute(query)
	songids.append(cursor.fetchone()[0])
	query = "select features_id from recommender_audiofeatures where " + dataType  + " < " + str(Aggregates[0]) + " order by random() limit 1"
	cursor.execute(query)
	songids.append(cursor.fetchone()[0])
	query = "select features_id from recommender_audiofeatures where " + dataType  + " > " + str(Aggregates[1]) + " order by random() limit 1"
	cursor.execute(query)
	songids.append(cursor.fetchone()[0])
	return songids
	

def getPrevious(request, datatype):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select "lowSongId", "midSongId", "highSongId" from "recommendationTest_preferredmusic" where id = ' + str(request.user.id)
	cursor.execute(query)
	ids = cursor.fetchone()
	attribs = []
	name = '"recommender_audiofeatures"'
	query = "select " + datatype + " from " + name + " where features_id = '" + ids[0] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	query = "select " + datatype + " from " + name + " where features_id = '" + ids[1] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	query = "select " + datatype + " from " + name + " where features_id = '" + ids[2] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	return attribs

def writePrevious(id, low, mid, high):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	name = '"recommendationTest_preferredmusic"'
	query = 'update "recommendationTest_preferredmusic" set "lowSongId" = ' + "'" + low + "'" + ', "midSongId" = '+ "'" + mid + "'" + ', "highSongId" = ' + "'" + high + "'" + ' where id = ' + str(id)
	cursor.execute(query)
	conn.commit()

def writeToPreferences(request, form, dataType, id):
	if form.is_valid():
		likeLow = form.cleaned_data['sampleOne']
		likeMid = form.cleaned_data['sampleTwo']
		likeHigh = form.cleaned_data['sampleThree']
		avgDiv = 0
		avgsum = 0
		attrib = 0
		previousSongAttribs = getPrevious(request, dataType)
		conn = psycopg2.connect(connectionString)
		cursor = conn.cursor()
		if likeLow:
			avgDiv = avgDiv + 1
			avgsum = previousSongAttribs[0]
		if likeMid:
			avgDiv = avgDiv + 1
			avgsum = avgsum + previousSongAttribs[1]
		if likeHigh:
			avgDiv = avgDiv + 1
			avgsum = avgsum + previousSongAttribs[2]
		if likeLow or likeMid or likeHigh:
			attrib = avgsum/avgDiv
		query = 'insert into "recommendationTest_preferredmusic" values (' + str(id) + ', '+ str(attrib) + ', 1.0, 1.0) on conflict (id) do update set "'+ dataType +'Preferred" = '+ str(attrib)
		cursor.execute(query)
		conn.commit()

def getRecs(dataType, id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	stddev = getAggregate(dataType)[3]
	query = 'select "' + dataType + 'Preferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	data = cursor.fetchone()[0]
	datalow = data - stddev
	datahigh = data + stddev
	query = 'select features_id from recommender_audiofeatures where "' + dataType + '" > ' + str(datalow) + ' and ' + dataType + ' < ' + str(datahigh) + ' order by random() limit 1'
	cursor.execute(query)
	return cursor.fetchone()[0]


def getPreferrences(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	return cursor.fetchone()
def tableEntry(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select exists(select 1 from "recommendationTest_preferredmusic" where id= ' + str(id) + ')'
	cursor.execute(query)
	if not cursor.fetchone()[0]:
		query = 'insert into "recommendationTest_preferredmusic" (id, "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred") values (' + str(id) + ', 0.5175604065506179, 0.5124401243104162, 116.89153340585992)'
		cursor.execute(query)
		conn.commit()
def RecPageOneView(request):
	Aggregates = getAggregate('danceability')
	user = request.user
	songids = findSong('danceability', Aggregates, user.explicit)
	form = genreForm()
	writePrevious(user.id, songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageTwoView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'danceability', user.id)
	Aggregates = getAggregate('acousticness')
	songids = findSong('acousticness', Aggregates, user.explicit)
	form2 = genreForm()
	writePrevious(user.id, songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageTwo.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageThreeView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'acousticness', user.id)
	Aggregates = getAggregate('tempo')
	songids = findSong('tempo', Aggregates, user.explicit)
	form2 = genreForm()
	writePrevious(user.id, songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageThree.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def ResultPageView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'tempo', user.id)
	data = getPreferrences(user.id)
	return render(request, 'recommendationPages//results.html', {'dance' : data[0], 'acousticness' : data[1], 'tempo' : data[2]})

def RecFinal(request):
	user = request.user
	dance = getRecs('danceability', user.id)
	acoustic = getRecs('acousticness', user.id)
	tempo = getRecs('tempo', user.id)
	return render(request, 'recommendationPages/recs.html', {'dance' : dance, 'acoustic' : acoustic, 'tempo' : tempo})
