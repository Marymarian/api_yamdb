from django.contrib import admin
from .models import Users, Title, Categories, Genres, Review, Comments

admin.site.register(Users)
admin.site.register(Title)
admin.site.register(Categories)
admin.site.register(Genres)
admin.site.register(Review)
admin.site.register(Comments)
