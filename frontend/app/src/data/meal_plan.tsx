import { Recipe, recipesDetail } from './recipe_detail';

export interface Meal {
    main_dish: Recipe;
    side_dish: Recipe;
    salad: Recipe; 
}

export interface MealPlan {
    id: number;
    servings_per_meal: number;
    creation_date: string;
    meals: Record<number, Meal>;
}

export const mealPlan: MealPlan = {
    "id": 1,
    "servings_per_meal": 2,
    "creation_date": "2024-02-25",
    "meals": {
        1: {
            "main_dish": recipesDetail["1"],
            "side_dish": recipesDetail["2"],
            "salad": recipesDetail["3"]
        },
        2: {
            "main_dish": recipesDetail["1"],
            "side_dish": recipesDetail["2"],
            "salad": recipesDetail["3"]
        },
        3: {
            "main_dish": recipesDetail["1"],
            "side_dish": recipesDetail["2"],
            "salad": recipesDetail["3"]
        },
    }
}
