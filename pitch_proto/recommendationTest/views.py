from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd

connectionString = "host=localhost dbname=pitch_db user=admin password=admin"
#since our data set is not changing, I found it better to hard code the aggregate functions rather
#than query them every time you need them
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
	elif dataType == 'energy':
		Aggregates.append(0.21558868176494178)
		Aggregates.append(0.7669964589764287)
		Aggregates.append(0.4912925703706923)
		Aggregates.append(0.27570388860573797)
		return Aggregates
	elif dataType == 'loudness':
		Aggregates.append(-18.336222829228397)
		Aggregates.append(-5.278392810677954)
		Aggregates.append(-11.807307819952968)
		Aggregates.append(6.528915009275161)
		return Aggregates
	elif dataType == 'speechiness':
		Aggregates.append(0.08092244415462105)
		Aggregates.append(0.1980039439596451)
		Aggregates.append(0.08092244415462105)
		Aggregates.append(0.11708149980502591)
		return Aggregates
	elif dataType == 'instrumentalness':
		Aggregates.append(0.2182890461397754)
		Aggregates.append(0.569813676693794)
		Aggregates.append(0.2182890461397754)
		Aggregates.append(0.35152463055401917)
		return Aggregates
	elif dataType == 'liveness':
		Aggregates.append(0.016313774935333092)
		Aggregates.append(0.44066625820485283)
		Aggregates.append(0.22849001657009402)
		Aggregates.append(0.21217624163475934)
		return Aggregates
	elif dataType == 'valence':
		Aggregates.append(0.21479793384534768)
		Aggregates.append(0.7809374054856164)
		Aggregates.append(0.49786766966548757)
		Aggregates.append(0.28306973582013895)
		return Aggregates

#This will find songs for a given data type and return three songs with its specific attribute parameters

def findSong(dataType, Aggregates):
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

#Given the previous song ids, this will return the arribute of those songs
#in order to use them in preferences	
# mid low high
def getPrevious(request, datatype):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	ids = request.session['oldSongs']
	attribs = []
	query = "select " + datatype + " from recommender_audiofeatures where features_id = '" + ids[1] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	query = "select " + datatype + " from recommender_audiofeatures where features_id = '" + ids[0] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	query = "select " + datatype + " from recommender_audiofeatures where features_id = '" + ids[2] + "'"
	cursor.execute(query)
	attribs.append(cursor.fetchone()[0])
	return attribs

#Will take the average of the requested songs arrtibute and write it to the DB
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
		query = 'insert into "recommendationTest_preferredmusic" values (' + str(id) + ', '+ str(attrib) + ', 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0 ,1.0) on conflict (id) do update set "'+ dataType +'Preferred" = '+ str(attrib)
		cursor.execute(query)
		conn.commit()
#will retrieve a song given a preference 
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
#quick Rec is a tool we use to ensure the querying time is not too long every you want 
#to see your recommendations, it builds a table of recommendations when you 
#create your account and finish the test, so that there is a small easy table to query
#from each time you need recommended songs
def buildQuickRec(user_id, song_id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'delete from "recommendationTest_quickrec" where user_id = ' + "'" + str(user_id) + "'"
	cursor.execute(query)
	conn.commit()
	query = 'insert into "recommendationTest_quickrec" values (' + str(user_id)  + ", '" + '{"' + str(song_id[0]) + '", "' + str(song_id[1]) + '", "' + str(song_id[2]) + '", "' + str(song_id[3]) + '", "' + str(song_id[4]) + '", "' + str(song_id[5]) + '", "' + str(song_id[6]) + '", "' + str(song_id[7]) + '", "' + str(song_id[8]) + '"}' + "'" + ')'
	cursor.execute(query)
	conn.commit()
def grabQuickRec(user_id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select songs from "recommendationTest_quickrec" where user_id  = ' + "'" + str(user_id) + "'"
	cursor.execute(query)
	songids = cursor.fetchall()
	return songids
#tool for gettingn a list of preferrences
def getPreferrences(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred", "energyPreferred", "loudnessPreferred", "speechinessPreferred", "instrumentalnessPreferred", "livenessPreferred", "valencePreferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	return cursor.fetchone()
#tool for creating proper tables on account creation
def tableEntry(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select exists(select 1 from "recommendationTest_preferredmusic" where id= ' + str(id) + ')'
	cursor.execute(query)
	if not cursor.fetchone()[0]:
		query = 'insert into "recommendationTest_preferredmusic" (id, "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred", "energyPreferred", "instrumentalnessPreferred", "livenessPreferred", "loudnessPreferred", "speechinessPreferred", "valencePreferred") values (' + str(id) + ', 0.5175604065506179, 0.5124401243104162, 116.89153340585992, 0.4912925703706923, 0.2182890461397754, 0.22849001657009402, -11.807307819952968, 0.08092244415462105, 0.49786766966548757)'
		cursor.execute(query)
		conn.commit()
		songids = []
		songids.append(getRecs('danceability', id))
		songids.append(getRecs('acousticness', id))
		songids.append(getRecs('tempo', id))
		songids.append(getRecs('energy', id))
		songids.append(getRecs('loudness', id))
		songids.append(getRecs('speechiness', id))
		songids.append(getRecs('instrumentalness', id))
		songids.append(getRecs('liveness', id))
		songids.append(getRecs('valence', id))
		buildQuickRec(id, songids)
#render requests for the test pages.
def RecPageOneView(request):
	Aggregates = getAggregate('danceability')
	user = request.user
	songids = findSong('danceability', Aggregates)
	form = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageTwoView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'danceability', user.id)
	Aggregates = getAggregate('acousticness')
	songids = findSong('acousticness', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageTwo.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageThreeView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'acousticness', user.id)
	Aggregates = getAggregate('energy')
	songids = findSong('energy', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageThree.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageFourView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'energy', user.id)
	Aggregates = getAggregate('loudness')
	songids = findSong('loudness', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageFour.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageFiveView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'loudness', user.id)
	Aggregates = getAggregate('speechiness')
	songids = findSong('speechiness', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageFive.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageSixView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'speechiness', user.id)
	Aggregates = getAggregate('instrumentalness')
	songids = findSong('instrumentalness', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageSix.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageSevenView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'instrumentalness', user.id)
	Aggregates = getAggregate('liveness')
	songids = findSong('liveness', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageSeven.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1]})

def RecPageEightView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'liveness', user.id)
	Aggregates = getAggregate('valence')
	songids = findSong('valence', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageEight.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def RecPageNineView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'valence', user.id)
	Aggregates = getAggregate('tempo')
	songids = findSong('tempo', Aggregates)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageNine.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2]})

def ResultPageView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'tempo', user.id)
	data = getPreferrences(user.id)
	return render(request, 'recommendationPages//results.html', {'dance' : data[0], 'acousticness' : data[1], 'tempo' : data[2], 'energy': data[3], 'loudness' : data[4], 'speechiness' : data[5], 'instrumentalness' : data[6], 'liveness' : data[7], 'valence' : data[8]})

def RecFinal(request):
	user = request.user
	songids = []
	songids.append(getRecs('danceability', user.id))
	songids.append(getRecs('acousticness', user.id))
	songids.append(getRecs('tempo', user.id))
	songids.append(getRecs('energy', user.id))
	songids.append(getRecs('loudness', user.id))
	songids.append(getRecs('speechiness', user.id))
	songids.append(getRecs('instrumentalness', user.id))
	songids.append(getRecs('liveness', user.id))
	songids.append(getRecs('valence', user.id))
	buildQuickRec(request.user.id, songids)
	return render(request, 'recommendationPages/recs.html', {'songids' : songids})
