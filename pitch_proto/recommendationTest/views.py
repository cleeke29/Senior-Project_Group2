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
def getPreferrences(id):
	conn = psycopg2.connect(connectionString)
	cursor = conn.cursor()
	query = 'select "danceabilityPreferred", "acousticnessPreferred", "tempoPreferred", "energyPreferred", "loudnessPreferred", "speechinessPreferred", "instrumentalnessPreferred", "livenessPreferred", "valencePreferred" from "recommendationTest_preferredmusic" where id = ' + str(id)
	cursor.execute(query)
	return cursor.fetchone()
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

def RecPageOneView(request):
	Aggregates = getAggregate('danceability')
	user = request.user
	songids = findSong('danceability', Aggregates, user.explicit)
	form = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test2/', 'attrib' : 'Danceability'})

def RecPageTwoView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'danceability', user.id)
	Aggregates = getAggregate('acousticness')
	songids = findSong('acousticness', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test3/', 'attrib' : 'Acousticness'})

def RecPageThreeView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'tempo', user.id)
	Aggregates = getAggregate('energy')
	songids = findSong('energy', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test4/', 'attrib' : 'Energy'})

def RecPageFourView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'energy', user.id)
	Aggregates = getAggregate('loudness')
	songids = findSong('loudness', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test5/', 'attrib' : 'Loudness'})

def RecPageFiveView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'loudness', user.id)
	Aggregates = getAggregate('speechiness')
	songids = findSong('speechiness', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test6/', 'attrib' : 'Speechiness'})

def RecPageSixView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'speechiness', user.id)
	Aggregates = getAggregate('instrumentalness')
	songids = findSong('instrumentalness', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test7/', 'attrib' : 'Instrumentalness'})

def RecPageSevenView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'instrumentalness', user.id)
	Aggregates = getAggregate('liveness')
	songids = findSong('liveness', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test8/', 'attrib' : 'Liveness'})

def RecPageEightView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'liveness', user.id)
	Aggregates = getAggregate('valence')
	songids = findSong('valence', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form2, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../test9/', 'attrib' : 'Valence'})

def RecPageNineView(request):
	form = genreForm(request.POST)
	user = request.user
	writeToPreferences(request, form, 'valence', user.id)
	Aggregates = getAggregate('tempo')
	songids = findSong('tempo', Aggregates, user.explicit)
	form2 = genreForm()
	request.session['oldSongs'] = songids
	return render(request, 'recommendationPages/RecPageOne.html', {'form' : form, 'songidMid' : songids[0], 'songidLow' : songids[1], 'songidHigh' : songids[2], 'nextUrl' : '../result/', 'attrib' : 'Tempo'})

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
