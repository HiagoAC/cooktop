/**
 * Schemas for the pantry API.
 */


export interface createPantryItemSchema {
    name: string,
    quantity: number,
    unit: string,
    expiration?: string
}