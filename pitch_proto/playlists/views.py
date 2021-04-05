from django.shortcuts import render
from .forms import *
import psycopg2
import csv
import pandas as pd
from .models import playlist

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
    return render(request, 'playlists.html', {'form' : form, 'displayedplaylists' : tempData})
    

def newPlaylist(request):

    form = playlistForm(request.POST)
    if form.is_valid():
        conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
        cursor = conn.cursor()
        description = form.cleaned_data['playlistdescription']
        query = "select count(*) from playlists_playlist"
        cursor.execute(query)
        newid = cursor.fetchone()[0]
        newid = newid + 1
        query = "insert into playlists_playlist values (" + str(newid) + ", '" + description + "', " + str(request.user.id) + ")"
        cursor.execute(query)
        conn.commit()
        query = "select description from playlists_playlist where user_id = " + str(request.user.id)
        cursor.execute(query)
        userplaylists = cursor.fetchall()
        tempData = []
        for playlist in userplaylists:
            tempData.append(playlist[0])
    return render(request, 'playlists.html', {'form' : form, 'displayedplaylists' : tempData})

# Create your views here.