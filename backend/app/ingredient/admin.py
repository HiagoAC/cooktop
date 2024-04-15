from django.contrib import admin

from ingredient.models import (
    Ingredient,
    IngredientInPantry,
    RecipeIngredient,
    ShoppingListItem
)


admin.site.register(Ingredient)
admin.site.register(IngredientInPantry)
admin.site.register(RecipeIngredient)
admin.site.register(ShoppingListItem)
