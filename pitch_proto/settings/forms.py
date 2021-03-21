from django import forms

class settingForm(forms.Form):
	DarkMode = forms.BooleanField(required = False)
	Explicit = forms.BooleanField(required = False)