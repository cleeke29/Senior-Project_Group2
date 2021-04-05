from django import forms

class playlistForm(forms.Form):
    playlistdescription = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
