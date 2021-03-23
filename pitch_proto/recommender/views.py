from recommender.forms import SearchForm
from django.shortcuts import render
from django.http import Http404, JsonResponse
from .models import *
from .forms import *
from django.views.decorators.http import require_POST, require_GET
import numpy as np



def find_albums(song = None, artist = None, album = None, from_year = None, to_year = None):
    query = Track.objects.filter(artists__icontains = artist)
    
    if song is not None:
        query = query.filter(track_name__icontains = song)

    if album is not None:
        query = query.filter(album_name__icontains = album)

    if from_year is not None:
        query = query.filter(year__gte = from_year)

    if to_year is not None:
        query = query.filter(year__lte = to_year)

    # if genre is not None:
    #     query = 

    return list(query.order_by('-track_popularity').values('track_id','track_name','year'))



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

        albums = find_albums(
                song,
                artist,
                album,
                from_year,
                to_year
            )
            
        if number_of_songs is not None:
            albums = list(np.random.permutation(albums[:10]))[:number_of_songs] 
        else:
            albums = list(np.random.permutation(albums[:10]))[:3]
         
        return render(request, 'recommender/searchform.html', {'form': form, 'albums': albums })
    else:
        raise Http404('Something went wrong')



@require_GET
def searchform_get(request):
    form = SearchForm()
    return render(request, 'recommender/searchform.html', {'form': form})

