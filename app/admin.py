# Register your models here.

from django.contrib import admin
from .models import Post, Comment, Noticias

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Noticias)