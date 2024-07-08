/**
 * Interfaces used throughout the project.
 */


export interface Ingredient {
    name: string;
    quantity: number;
    display_unit: string;
}

export type ShoppingListItem {
    name: string;
    quantity: number;
    unit: string;
}

export interface Recipe {
    id: number;
    title: string;
    time_minutes: number;
    tags: string[];
    directions: string[];
    description: string;
    recipe_type: string;
    notes: string;
    ingredients: Ingredient[];
}

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
