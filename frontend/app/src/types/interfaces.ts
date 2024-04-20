/**
 * Interfaces used throughout the project.
 */


export interface Ingredient {
    name: string;
    quantity: number;
    display_unit: string;
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