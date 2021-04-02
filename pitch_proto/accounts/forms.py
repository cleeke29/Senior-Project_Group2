from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields =('username', 'email')

class AddFriendForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), max_length=150, required=False)
        
