from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Friend_Request, User
from django.http import HttpResponse

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

# Create your views here.
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

@login_required
def friends_list(request):
    allusers = User.objects.all()
    all_friend_requests = Friend_Request.objects.all()
    my_friends = request.user.friends.all()
    my_requests = all_friend_requests.filter(from_user_id=request.user.id).values_list('to_user_id', flat=True)
    my_pending = all_friend_requests.filter(to_user_id=request.user.id).values_list('from_user_id', flat=True)
    return render(request, 'friends.html', {'allusers': allusers,
                                            'all_friend_requests': all_friend_requests,
                                            'my_friends': my_friends,
                                            'my_requests': my_requests,
                                            'my_pending': my_pending}
                                            )