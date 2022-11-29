from django.contrib import admin

from .models import User, Titles, Categories, Genres, Reviews, Comments

admin.site.register(User)
admin.site.register(Titles)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Reviews)
admin.site.register(Comments)
