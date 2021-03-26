from django import forms

class SearchForm(forms.Form):
    song = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    artist = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    album = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}), required=False)
    from_year = forms.IntegerField(required=False)
    to_year = forms.IntegerField(required=False)
    # genre = forms.CharField(widget=forms.TextInput(attrs={'size': '50'}))
    number_of_songs = forms.IntegerField(required=False)