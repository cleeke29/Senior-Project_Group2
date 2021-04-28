from django.shortcuts import render, redirect
from .forms import *
import psycopg2
import csv
import pandas as pd
from .models import playlist
#load playlist page
def playlists(request):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select description from playlists_playlist where user_id = " + str(request.user.id)
    cursor.execute(query)
    userplaylists = cursor.fetchall()
    tempData = []

    for playlist in userplaylists:
        tempData.append(playlist[0])
    form = playlistForm()
    return render(request, 'playlists.html', {'form' : form, 'displayedplaylists' : tempData, 'userid' : request.user.id, 'host': request.get_host()})
    
#create new playlist
def newPlaylist(request):

    form = playlistForm(request.POST)
    if form.is_valid():
        conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
        cursor = conn.cursor()
        description = form.cleaned_data['playlistdescription']
        query = "select id from playlists_playlist order by id desc limit 1"
        cursor.execute(query)
        tempnewid = cursor.fetchone()
        if tempnewid is not None:
            newid = tempnewid[0]
            newid = newid + 1
        else:
            newid = 1
        query = "insert into playlists_playlist values (" + str(newid) + ", '" + description + "', " + str(request.user.id) + ")"
        cursor.execute(query)
        conn.commit()
    return redirect("/playlists/playlists/")
#display playlist on page
def displayPlaylist(request, list):
    tempData = getSongsInList(list, request.user.id)
    return render(request, 'playlistdisplay.html', {'playlistsongs': tempData, 'playlist': list})
#get songs in a playlist
def getSongsInList(list, userid):
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select id from playlists_playlist where description = '" + list + "' and user_id = " + str(userid)
    cursor.execute(query)
    id = cursor.fetchone()[0]
    query = "select track_id from playlists_playlist_songs where playlist_id = " + str(id)
    cursor.execute(query)
    songs = cursor.fetchall()
    tempData = []
    for song in songs:
        tempData.append(song[0])
    return tempData

#reloads playlist display page after deleting song
def removeSong(request, list, song):
    remSong(list, song, request.user.id)
    return redirect("/playlists/playlists/" + list + "/")
#<<<<<<< HEAD

#def remSong(list, song, user):
#=======
#removes song from playlist
def remSong(list, song):
#>>>>>>> 40ed088393a422615cda228006adb49a412752b3
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "select id from playlists_playlist where description = '" + list + "' and user_id = " + str(user)
    cursor.execute(query)
    id = cursor.fetchone()[0]
    query = "delete from playlists_playlist_songs where track_id = '" + song + "' and playlist_id = " + str(id)
    cursor.execute(query)
    conn.commit()
    
#removes all songs in playlist and then deletes playlist
def removePlaylist(request, list):
    tempData = getSongsInList(list, request.user.id)
    for song in tempData:
        remSong(list, song, request.user.id)
    conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
    cursor = conn.cursor()
    query = "delete from playlists_playlist where description = '" + list + "' and user_id = " + str(request.user.id)
    cursor.execute(query)
    conn.commit()
    
    return redirect("/playlists/playlists/")
#Copy a playlist from one user to another via share link
def copyPlaylist(request, list, id):
    recipientid = request.user.id
    if recipientid != id:
        conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
        cursor = conn.cursor()
        query = "select id from playlists_playlist order by id desc limit 1"
        cursor.execute(query)
        newplaylistid = cursor.fetchone()[0]
        newplaylistid = newplaylistid + 1

        query = "insert into playlists_playlist values (" + str(newplaylistid) + ", '" + list + "', " + str(recipientid) + ")"
        cursor.execute(query)
        conn.commit()
        
        query = "select id from playlists_playlist where description = '" + list + "' and user_id = " + str(id)
        cursor.execute(query)
        bridgingid = cursor.fetchone()[0]
        query = "select track_id from playlists_playlist_songs where playlist_id = " + str(bridgingid)
        cursor.execute(query)
        songs = cursor.fetchall()
        tempData = []
        for song in songs:
            tempData.append(song[0])
        for songid in tempData:
            query = "select id from playlists_playlist_songs order by id desc limit 1"
            cursor.execute(query)
            newid = cursor.fetchone()[0]
            newid = newid + 1
            query = "insert into playlists_playlist_songs values (" + str(newid) + ", " + str(newplaylistid) + ", '" + songid + "')"
            cursor.execute(query)
            conn.commit()
    return redirect("/playlists/playlists/")
# Create your views here.
