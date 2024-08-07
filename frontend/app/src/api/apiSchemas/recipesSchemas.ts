/**
 * Schemas for the recipes API.
 */

import { Ingredient } from '../../types/interfaces';
import { recipeTypeLabels } from '../../types/constants';


export interface RecipeIn {
    title: string;
    time_minutes: number | null;
    tags: string[];
    directions: string[];
    description: string | null;
    recipe_type: keyof typeof recipeTypeLabels;
    notes: string | null;
    ingredients: Ingredient[];
}

export type RecipePatch = Partial<RecipeIn>;

export interface RecipeListInfo {
    id: number;
    title: string;
    time_minutes: number;
    tags: string[];
}

export interface RecipeFilters {
    ingredients?: string[];
    tags?: string[];
    recipe_type?: keyof typeof recipeTypeLabels;
}