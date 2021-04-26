from recommender.forms import SearchForm
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import numpy as np
from django.core.paginator import Paginator
import psycopg2
import csv
import pandas as pd
import re
import datetime



def find_albums(number_of_songs = None, song = None, artist = None, album = None, from_year = None, to_year = None):
    query = Track.objects.all()
    if artist is not None:
        query = query.filter(artists__icontains = artist)
    
    if song is not None:
        query = query.filter(track_name__icontains = song)

    if album is not None:
        query = query.filter(album_name__icontains = album)

    if from_year is not None:
        query = query.filter(year__gte = from_year)

    if to_year is not None:
        query = query.filter(year__lte = to_year)

    if number_of_songs is None:
        number_of_songs = 10
    # if genre is not None:
    #     query = 

    return query.order_by('-track_popularity').values('track_id')[:number_of_songs]



@require_POST
def searchform_post(request):
    # create a form instance and populate it with data from the request:
    form = SearchForm(request.POST)
    # check whether it's valid:
    if form.is_valid():
        # process the data in form.cleaned_data as required
        song = None if form.cleaned_data['song'] == None else form.cleaned_data['song']
        artist = None if form.cleaned_data['artist'] == None else form.cleaned_data['artist']
        album = None if form.cleaned_data['album'] == None else form.cleaned_data['album']
        from_year = None if form.cleaned_data['from_year'] == None else int(form.cleaned_data['from_year'])
        to_year = None if form.cleaned_data['to_year'] == None else int(form.cleaned_data['to_year'])
        # genre = None if form.cleaned_data['genre'] == None else form.cleaned_data['genre']
        number_of_songs = None if form.cleaned_data['number_of_songs'] == None else int(form.cleaned_data['number_of_songs'])
        args = {
            'song': song,
            'artist': artist,
            'album': album,
            'from_year': from_year,
            'to_year': to_year,
            'number_of_songs': number_of_songs
        }
        # albums = find_albums(
        #         number_of_songs,
        #         song,
        #         artist,
        #         album,
        #         from_year,
        #         to_year
        #     )
        # page = request.GET.get('page', 1)
        # paginator = Paginator(albums, 3)
        # songs = paginator.page(page)
        # if number_of_songs is not None:
        #     albums = list(np.random.permutation(albums[:10]))[:number_of_songs] 
        # else:
        #     albums = list(np.random.permutation(albums[:10]))[:3]
        request.session['export_query'] = args
        return redirect('results')
    else:
        raise Http404('Something went wrong')



@require_GET
def searchform_get(request):
    form = SearchForm()
    return render(request, 'recommender/searchform.html', {'form': form})


def results(request):
    
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    if 'add_to_playlist' in request.POST:
        pass
        playlist = request.POST['playlists']
        song = request.POST['SongID']
        query = "select id from playlists_playlist where description = '" + playlist + "' and user_id = " + str(request.user.id)
        cursor.execute(query)
        playlistid = cursor.fetchone()
        print(str(playlistid[0]) + ', ' + song)
        query = "select id from playlists_playlist_songs order by id desc limit 1"
        cursor.execute(query)
        newid = cursor.fetchone()[0]
        newid = newid + 1
        query = "insert into playlists_playlist_songs values (" + str(newid) + ", " + str(playlistid[0]) + ", '" + song + "')"
        cursor.execute(query)
        conn.commit()
        
    query = "select description from playlists_playlist where user_id = " + str(request.user.id)
    cursor.execute(query)
    userplaylists = cursor.fetchall()
    tempData = []
    for playlist in userplaylists:
        tempData.append(playlist[0])
    
    data = request.session['export_query']
    albums = find_albums(
        data['number_of_songs'],
        data['song'],
        data['artist'],
        data['album'],
        data['from_year'],
        data['to_year']
    )
    page = request.GET.get('page', 1)
    paginator = Paginator(albums, 3)
    songs = paginator.page(page)

    return render(request, 'recommender/search_results.html', {'albums': songs, 'playlistdescriptions': tempData})


def searchSong(request, song_name):
    song = song_name
    artist = None
    album = None
    from_year = None
    to_year = None
    number_of_songs = None
    args = {
        'song': song,
        'artist': artist,
        'album': album,
        'from_year': from_year,
        'to_year': to_year,
        'number_of_songs': number_of_songs
    }
    request.session['export_query'] = args
    return redirect('results')

class commentObject:
    def __init__(self, username, text):
        self.username = username
        self.text = text

def getComments(track):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select * from recommender_comment where track_id = '" + str(track) + "' order by commentid DESC"
    cursor.execute(query)
    return cursor.fetchall()
def discuss(request, track):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select exists(select 1 from recommender_comment where track_id = '" + str(track) + "')"
    cursor.execute(query)
    exists = cursor.fetchone()
    form = commentForm()
    query = "select track_name from recommender_track where track_id = '" + str(track) + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    if(exists[0]):
        comments = getComments(track)
        usernames = []
        texts = []
        for entry in comments:
            usernames.append(entry[1])
            texts.append(entry[2])
        commentarray = []
        x = len(comments) - 1
        while(x >= 0):
            commentarray.append(commentObject(usernames[x], texts[x]))
            x = x - 1
        return render(request, 'recommender/discuss.html', {'exists' : 'True', 'track_id' : track, 'form' : form, 'track_name' : data[0], 'comments' : commentarray})
    return render(request, 'recommender/discuss.html', {'exists' : 'False', 'track_id' : track, 'form' : form, 'track_name' : data[0]})

def startDiscuss(request, track):
    form = commentForm(request.POST)
    text = ''
    if form.is_valid():
        text = form.cleaned_data['comment']
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "insert into recommender_comment (track_id, username, text) values ('" + str(track)  + "', '" + str(request.user.username) + "', '" + str(text) + "')"
    cursor.execute(query)
    conn.commit()
    query = "select track_name from recommender_track where track_id = '" + str(track) + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    comments = getComments(track)
    usernames = []
    texts = []
    for entry in comments:
        usernames.append(entry[1])
        texts.append(entry[2])
    commentarray = []
    x = len(comments) - 1
    while(x >= 0):
        commentarray.append(commentObject(usernames[x], texts[x]))
        x = x - 1
    return render(request, 'recommender/discuss.html', {'exists' : 'True', 'track_id' : track, 'form' : form, 'track_name' : data[0], 'comments' : commentarray})
    

def Song_info(request, track):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select * from recommender_track where track_id = '" + str(track) + "'"
    cursor.execute(query)
    data = cursor.fetchone()
    artists = re.findall(r"\'(.*?)\'", data[0])
    return render(request, 'recommender/browse.html', { 'artists' : artists, 
                                                        'track_id' : track,
                                                        'track_name' : data[1],
                                                        'album_name' : data[3],
                                                        'explicit' : data[4],
                                                        'years' : data[6],
                                                        'track_number' : data[7]})

def Album_info(request, album):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select DISTINCT on (track_number) track_name, track_id, artists, explicit, year, track_number from recommender_track where album_name = '" + album + "'" 
    cursor.execute(query)
    data = cursor.fetchall()
    names = []
    ids = []
    artists = []
    explicits = []
    years = []
    track_numbers = []
    for entry in data:
        names.append(entry[0])
        ids.append(entry[1])
        artists.append(re.findall(r"\'(.*?)\'", entry[2]))
        explicits.append(entry[3])
        years.append(entry[4])
        track_numbers.append(entry[5])
    class songObject:
        def __init__(self, name, id, artist, explicit, year, track_number):
            self.name = name
            self.id = id
            self.artist = artist
            self.explicit = explicit
            self.year = year
            self.track_number = track_number

    newData = []
    x = len(names) - 1
    while (x >= 0):
        newData.append(songObject(names[x], ids[x], artists[x], explicits[x], years[x], track_numbers[x]))
        x = x - 1
        #'names' : names, 'ids' : ids, 'artists' : artists, 'explicits' : explicits, 'years' : years, 'track_numbers' : track_numbers
    return render(request, 'recommender/album_info.html', {'data' : newData, 'album' : album})
# @require_POST
# def display_album(request):
#     conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
#     cursor = conn.cursor()
#     query = "SELECT track_id, track_number, track_name, REPLACE((REPLACE((REPLACE(artists, '[', '')), ']', '')), ''', ''), album_name, year FROM recommender_track WHERE track_id = " + track_id
#     cursor.execute(query)
#     conn.commit()
