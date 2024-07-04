/**
 * Schemas for the meal plans API.
 */


export interface createMealPlanSchema {
    requested_ingredients: string[],
    cookings?: number,
    servings_per_meal?: number
}