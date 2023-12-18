from django.contrib import admin

from ingredient.models import Ingredient, IngredientInPantry


admin.site.register(Ingredient)
admin.site.register(IngredientInPantry)
