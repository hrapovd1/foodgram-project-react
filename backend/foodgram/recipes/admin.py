from django.contrib import admin
from django.contrib.auth.models import Group

from .models import User, Tag, Recipe

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Recipe)
