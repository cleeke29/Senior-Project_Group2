from recommender.forms import SearchForm
from django.shortcuts import render, redirect
from django.http import Http404, JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import numpy as np
from django.core.paginator import Paginator



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

# @require_POST
# def display_album(request):
#     conn = psycopg2.connect("host=localhost dbname=pitch_db user=admin password=admin")
#     cursor = conn.cursor()
#     query = "SELECT track_id, track_number, track_name, REPLACE((REPLACE((REPLACE(artists, '[', '')), ']', '')), ''', ''), album_name, year FROM recommender_track WHERE track_id = " + track_id
#     cursor.execute(query)
#     conn.commit()
