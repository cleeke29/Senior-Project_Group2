from django.urls import path 
from .views import SignUpView, accept_friend_request, send_friend_request, friends_list, ProfilePageView, EditProfileView, profileRedirectView, deleteRequest, deleteFriend, findUser, follow, unfollow, followList, goToUser
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
    path('<int:pk>/profile/', ProfilePageView.as_view(), name='profile'),
    path('<int:pk>/edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('profile/', profileRedirectView, name='find_profile'),
    path('delete_friend_request/<str:pk>/', deleteRequest, name="delete_request"),
    path('delete_friend/<int:friendID>/', deleteFriend, name="delete_friend"),
    path('findUser/', findUser, name="find_user"),
    path('follow/<int:userID>/', follow, name='follow'),
    path('unfollow/<int:userID>/', unfollow, name='unfollow'),
    path('follow-list/', followList, name='follow-list'),
    path('go-to-user/<int:userID>/', goToUser, name='go_to_user')
]
