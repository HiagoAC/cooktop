from django.contrib import admin

from meal_plan.models import Preferences, Meal, MealPlan


admin.site.register(Preferences)
admin.site.register(Meal)
admin.site.register(MealPlan)
