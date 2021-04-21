from django.urls import path
from . import views

urlpatterns = [ 
    path('partyroom/<str:user_id>/', views.partyroom, name='partyroom'),
    path('party_invites/', views.see_invites, name='party_invites'),
]