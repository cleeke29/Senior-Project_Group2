from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd


def getAggregate(dataType):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	Aggregates = []
	query = "select avg(" + dataType + ") - stddev(" + dataType + ") from recommender_audiofeatures"
	cursor.execute(query)
	Aggregates.append(cursor.fetchone()[0])
	query = "select avg(" + dataType + ") + stddev(" + dataType + ") from recommender_audiofeatures"
	cursor.execute(query)
	Aggregates.append(cursor.fetchone()[0])
	query = "select avg(" + dataType + ") from recommender_audiofeatures"
	cursor.execute(query)
	Aggregates.append(cursor.fetchone()[0])
	# aggregates[0] = lower bound, aggregate[1] = higher bound, aggregate[2] = average
	return Aggregates



def findSong(dataType, Aggregates):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
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
	

def getPrevious(datatype):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = ('select "lowSongId", "midSongId", "highSongId" from "recommendationTest_holdmydata" where id = 1')
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

def writePrevious(low, mid, high):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	name = '"recommendationTest_holdmydata"'
	query = 'delete from "recommendationTest_holdmydata" where id = 1'
	cursor.execute(query)
	query = "insert into " + name + " values (1, '" + low +"', '" + mid + "', '" + high + "')"
	cursor.execute(query)
	conn.commit()

def writeToPreferences(form, dataType, id):
	if form.is_valid():
		likeLow = form.cleaned_data['sampleOne']
		likeMid = form.cleaned_data['sampleTwo']
		likeHigh = form.cleaned_data['sampleThree']
		avgDiv = 0
		avgsum = 0
		attrib = 0
		previousSongAttribs = getPrevious(dataType)
		conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
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
		query = 'update "recommendationTest_preferredmusic" set "'+ dataType +'Preferred" = '+ str(attrib) +' where id = ' + str(id)
		cursor.execute(query)
		conn.commit()

def getRecs(dataType, id):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'select stddev("' + dataType + '") from recommender_audiofeatures'
	cursor.execute(query)
	stddev = cursor.fetchone()[0]
	query = 'select "' + dataType + 'Preferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	data = cursor.fetchone()[0]
	datalow = data - stddev
	datahigh = data + stddev
	query = 'select features_id from recommender_audiofeatures where "' + dataType + '" > ' + str(datalow) + ' and ' + dataType + ' < ' + str(datahigh) + ' order by random() limit 1'
	cursor.execute(query)
	return cursor.fetchone()[0]


def getPreferrences(id):
	conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
	cursor = conn.cursor()
	query = 'select "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	return cursor.fetchone()

def RecPageOneView(request):
	Aggregates = getAggregate('danceability')
	songids = findSong('danceability', Aggregates)
	form = genreForm()
	writePrevious(songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageTwoView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(form, 'danceability', user.id)
	Aggregates = getAggregate('acousticness')
	songids = findSong('acousticness', Aggregates)
	form2 = genreForm()
	writePrevious(songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageTwo.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageThreeView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(form, 'acousticness', user.id)
	Aggregates = getAggregate('tempo')
	songids = findSong('tempo', Aggregates)
	form2 = genreForm()
	writePrevious(songids[1], songids[0], songids[2])
	return render(request, 'recommendationPages/RecPageThree.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def ResultPageView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(form, 'tempo', user.id)
	data = getPreferrences(user.id)
	return render(request, 'recommendationPages//results.html', {'dance' : data[0], 'acousticness' : data[1], 'tempo' : data[2]})

def RecFinal(request):
	user = request.user
	dance = getRecs('danceability', user.id)
	acoustic = getRecs('acousticness', user.id)
	tempo = getRecs('tempo', user.id)
	return render(request, 'recommendationPages/recs.html', {'dance' : dance, 'acoustic' : acoustic, 'tempo' : tempo})