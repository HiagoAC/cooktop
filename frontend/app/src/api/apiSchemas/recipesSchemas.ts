/**
 * Schemas for the recipes API.
 */

import { Ingredient } from '../../types/interfaces';
import { recipeTypes } from '../../types/constants';


export interface RecipeIn {
    title: string;
    time_minutes: number | null;
    tags: string[];
    directions: string[];
    description: string | null;
    recipe_type: keyof typeof recipeTypes;
    notes: string | null;
    ingredients: Ingredient[];
}

export interface RecipeListInfo {
    id: number;
    title: string;
    time_minutes: number;
    tags: string[];
}