from django import forms

class genreForm(forms.Form):
	sampleOne = forms.BooleanField(required = False)
	sampleTwo = forms.BooleanField(required = False)
	sampleThree = forms.BooleanField(required = False)