from django.shortcuts import render
import requests

def partyroom(request):
    return render(request, 'partyroom/partyroom.html')

# Create your views here.
