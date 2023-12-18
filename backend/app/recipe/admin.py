from django.contrib import admin

from recipe.models import Recipe, Tag


admin.site.register(Recipe)
admin.site.register(Tag)
