from django.contrib import admin
from .models import Cmux, Tag, Author, Vote

admin.site.register(Cmux)
admin.site.register(Tag)
admin.site.register(Author)
admin.site.register(Vote)
