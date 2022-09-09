from django.contrib import admin
from Netflixapp.models import Movie,Video,Profile,CustomUser,Webseries,webseriesepisodes


admin.site.register(Movie)
admin.site.register(Video)
admin.site.register(Profile)
admin.site.register(CustomUser)
admin.site.register(Webseries)
admin.site.register(webseriesepisodes)