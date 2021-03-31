from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import Friend_Request, User
from django.http import HttpResponse
from django.db.models import Q 

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
    allusers = User.objects.all().filter(is_superuser=False).exclude(id=request.user.id)
    my_friends = request.user.friends.all()
    all_friend_requests = Friend_Request.objects.all().filter(from_user_id=request.user.id)
    my_pending = Friend_Request.objects.all().filter(to_user_id=request.user.id)
    

    my_requests_vals = all_friend_requests.filter(from_user_id=request.user.id).values_list('to_user_id', flat=True)
    friend_vals = my_friends.values_list('id', flat=True)
    my_pending_vals = my_pending.values_list('from_user_id', flat=True)
    may_know = allusers.exclude(id__in=my_requests_vals).exclude(id__in=my_pending_vals).exclude(id__in=friend_vals)
    
    return render(request, 'friends.html', {'all_friend_requests': all_friend_requests,
                                            'my_friends': my_friends,
                                            'my_pending': my_pending,
                                            'may_know': may_know}
                                            )

def profileRedirectView(request):
    return redirect('http://localhost:8000/accounts/' + str(request.user.id) + '/profile')


class EditProfileView(UpdateView):
    model = User
    template_name = 'edit_profile.html'
    success_url = reverse_lazy('find_profile')
    fields = ['bio', 'image']

class ProfilePageView(DetailView):
    model = User
    template_name = 'profile.html'

    def get_context_data(self, *args, **kwargs):
        users = User.objects.all()
        context = super(ProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(User, id=self.kwargs['pk'])
        context["page_user"] = page_user
        return context
