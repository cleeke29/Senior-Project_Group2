from django.contrib import admin
from .models import Categories, Artist, Album, AudioFeatures,Track, Genres

# Register your models here.
admin.site.register(Categories)
admin.site.register(Artist)
admin.site.register(Album)
admin.site.register(AudioFeatures)
admin.site.register(Track)
admin.site.register(Genres)
