from django.urls import path 
from .views import SignUpView, accept_friend_request, send_friend_request, friends_list
from django.views.generic.base import TemplateView

urlpatterns = [ 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('friends/', friends_list, name='friends'),
    path('send_friend_request/<int:userID>/',
        send_friend_request,
        name='send_friend_request'),
    path('accept_friend_request/<int:requestID>/',
        accept_friend_request,
        name='accept_friend_request'),
]
