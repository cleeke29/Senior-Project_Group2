from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .forms import CustomUserCreationForm, AddFriendForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Friend_Request, User, Follows
from django.http import HttpResponse
from django.db.models import Q 

#SignUpView is a class-based view for the user signup form. Redirects to login the user on success.
class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

#send_friend_request allows a user to send a friend request to the specified user ID.
@login_required
def send_friend_request(request, userID):
    from_user = request.user
    to_user = User.objects.get(id=userID)
    friend_request, created = Friend_Request.objects.get_or_create(
        from_user=from_user, to_user=to_user
    )
    return redirect('friends')
    # if created:
    #     return HttpResponse('friend request sent')
    # else:
    #     return HttpResponse('friend request was already sent')

#accept_friend_request allows the requesting user to accept a specified friend request, creating the friendship relation between them and the other user.
@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
    return redirect('friends')
    #     return HttpResponse('friend request accepted')
    # else:
    #     return HttpResponse('friend request not accepted')

#friends_list is a view for the Friends page. Provides data for friend requests that are outgoing/incoming, a list of users to add as a friend, 
#   a list of the user's friends, and the form object used to add a user by their username.
@login_required
def friends_list(request):
    allusers = User.objects.all().filter(is_superuser=False).exclude(id=request.user.id)
    my_friends = request.user.friends.all()
    all_friend_requests = Friend_Request.objects.all().filter(from_user_id=request.user.id)
    my_pending = Friend_Request.objects.all().filter(to_user_id=request.user.id)
    
    form = AddFriendForm()

    my_requests_vals = all_friend_requests.filter(from_user_id=request.user.id).values_list('to_user_id', flat=True)
    friend_vals = my_friends.values_list('id', flat=True)
    my_pending_vals = my_pending.values_list('from_user_id', flat=True)
    may_know = allusers.exclude(id__in=my_requests_vals).exclude(id__in=my_pending_vals).exclude(id__in=friend_vals)
    
    return render(request, 'friends.html', {'all_friend_requests': all_friend_requests,
                                            'my_friends': my_friends,
                                            'my_pending': my_pending,
                                            'may_know': may_know,
                                            'form' : form
                                            }
                                            )

#profileRedirectView redirects to the request user's profile
def profileRedirectView(request):
    return redirect('https://pitchmusic.ddns.net/accounts/' + str(request.user.id) + '/profile')

#EditProfileView is a class-based view for the Edit profile form for a user. Can alter bio/profile picture fields. Returns user to their profile on success.
class EditProfileView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('find_profile')
    fields = ['bio', 'image']

#ProfilePageView is a class-based view for the profile page of a user. 
#   Pfp is passed context data that includes followers/following + the count of each, a count of the user's friends, 
#       and the user who's profile we are viewing.
class ProfilePageView(DetailView):
    model = User
    template_name = 'profile.html'

    ''' 
        Context Data:
        page_user is the user who's information is displayed
        following is a list of rows from the Follows table where data shows the page_user as a follower
        followers is a list of rows from the Follows table where data shows the page_user as being followed
        followers_list is a list of user objects that are following the page_user
        following_list is a list of user objects that the page_user is following
        followed_by_user and follows_user are the following and followers count respectively
        friends is a count of how many friends a user has
        
        The generated page can use page_user, followers_list, following_list, followed_by_user, friends and follows_user
    '''
    def get_context_data(self, *args, **kwargs):
        users = User.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        following = Follows.objects.all().filter(follower_id=page_user.id)
        followers = Follows.objects.all().filter(following_id=page_user.id)
        followers_list = []
        following_list = []
        for follower in followers:
            followers_list.append(User.objects.get(id=follower.follower_id))
        for follow in following:
            following_list.append(User.objects.get(id=follow.following_id))
        followed_by_user = following.count()
        follows_user = followers.count()
        friends = page_user.friends.all().count()
        context["page_user"] = page_user
        context["num_following"] = followed_by_user
        context["num_followers"] = follows_user
        context["following"] = following_list
        context["followers"] = followers_list
        context["friends"] = friends
        return context
    
#deleteRequest deletes an existing, specified friend request.
def deleteRequest(request, pk):
    request_data = Friend_Request.objects.get(id=pk)
    request_data.delete()
    return redirect('friends')

#deleteFriend function is used to remove the friendship relation from the requesting user and the user with the specified id.
def deleteFriend(request, friendID):
    friendship = request.user.friends.get(id = friendID)
    request.user.friends.remove(friendship)
    friendship.friends.remove(request.user)
    return redirect('friends')

#findUser is used by the form on the Friends page. The form passes a string, and we attempt to find a username to match
#   then we send a friend request to the user if one is found.
def findUser(request):
    form = AddFriendForm(request.POST)
    if form.is_valid():
        name = None if form.cleaned_data['username'] == None else form.cleaned_data['username']
        friends = request.user.friends.all()
        my_pending = Friend_Request.objects.all().filter(to_user_id=request.user.id)
        all_friend_requests = Friend_Request.objects.all().filter(from_user_id=request.user.id)
        if name != request.user.username and name:
            try:
                friend = User.objects.get(username = name)
                if friend not in friends:
                    #print("\n\nHERE\n\n")
                    # print(my_pending.values_list('from_user_id', flat=True))
                    # print(all_friend_requests.values_list('to_user_id', flat=True))
                    if friend.id in my_pending.values_list('from_user_id', flat=True):
                        request.user.friends.add(friend)
                        friend.friends.add(request.user)
                        Friend_Request.objects.filter(from_user_id=friend.id).filter(to_user_id=request.user.id).get().delete()
                    else:
                        send_friend_request(request, friend.id)
            except: 
                print("User does not exist")
    return redirect('friends')

#follow function allows a user to follow a specified user by their ID
@login_required
def follow(request, userID):
    follower = request.user
    following = User.objects.get(id=userID)
    relationship, created = Follows.objects.get_or_create(
        follower=follower, following=following
    )
    return redirect('https://pitchmusic.ddns.net/accounts/' + str(userID) + '/profile/')

#unfollow function allows a user to unfollow a specified user by ID.
@login_required
def unfollow(request, userID):
    relationship = Follows.objects.all().filter(follower_id=request.user.id, following_id=userID)
    relationship.delete()
    return redirect('https://pitchmusic.ddns.net/accounts/' + str(userID) + '/profile/')

#followList provides information about followers/following for the Following page of the site
def followList(request):
    following = Follows.objects.all().filter(follower_id=request.user.id)
    followers = Follows.objects.all().filter(following_id=request.user.id)
    followers_list = []
    following_list = []
    for follower in followers:
        followers_list.append(User.objects.get(id=follower.follower_id))
    for follow in following:
        following_list.append(User.objects.get(id=follow.following_id))

    return render(request, 'follow-list.html', {'followers': followers_list,
                                            'following': following_list,
                                            }
                                            )
# Function is called to bring user to a specified user's profile page
def goToUser(request, userID):
    return redirect('https://pitchmusic.ddns.net/accounts/'+ str(userID) + '/profile/')
