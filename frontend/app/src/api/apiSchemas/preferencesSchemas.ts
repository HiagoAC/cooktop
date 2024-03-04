/**
 * Schemas for the preferences API.
 */


export interface preferencesSchema {
    servings_per_meal: number,
    cookings_per_week: number,
}

export interface preferencesPartialSchema {
    servings_per_meal?: number,
    cookings_per_week?: number,
}
