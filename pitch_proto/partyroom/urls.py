from django.urls import path
from . import views

urlpatterns = [ 
    path('partyroom/', views.partyroom, name='partyroom'),
    
]