from django.db import models

class usersettings(models.Model):
	darkmode = models.BooleanField()
	explicit = models.BooleanField()
	