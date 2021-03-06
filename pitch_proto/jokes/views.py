from django.shortcuts import render
import requests

def index(request):
    url = 'http://api.icndb.com/jokes/random/'
    response = requests.get(url).json()
    joke = response['value']['joke']
    return render(request, 'jokes/jokes.html')
