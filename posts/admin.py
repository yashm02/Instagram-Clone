from __future__ import absolute_import

from django.contrib import admin

from .models import Post,Comment



admin.site.register(Post)
admin.site.register(Comment)
