from django import urls
from django.shortcuts import render
import requests
from .models import Listening_Room, Room_Invite
from django.conf import settings
import os

def partyroom(request, user_id):
    """
    This creates a room in the database specific to the user.
    """
    room_instance = Listening_Room.objects.get_or_create(
        dj=request.user.username, 
        link_address=os.path.join(request.get_host(), f'group/partyroom/{request.user}/')
        )
    return render(request, 'partyroom/partyroom.html', {'user_id': user_id})

def attend(request, user_id):
    """
    This loads a partyroom created by someone else
    """
    return render(request, 'partyroom/partyroom.html', {'user_id': user_id})

def see_invites(request):
    """
    shows the available rooms for a user to join
    """
    my_friends = request.user.friends.all().values_list('username', flat=True)
    rooms = Listening_Room.objects.all()
    return render(request, 'partyroom/party_invites.html',{'friends': my_friends,
                                                            'rooms': rooms})

# Create your views here.
