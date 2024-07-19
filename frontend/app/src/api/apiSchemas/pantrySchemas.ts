/**
 * Schemas for the pantry API.
 */


export interface createPantryItemSchema {
    name: string,
    quantity: number,
    unit: string,
    expiration?: string
}

export interface updatePantryItemSchema {
    id: number,
    name?: string,
    quantity?: number,
    unit?: string,
    expiration?: string
}

export interface subtractFromPantrySchema {
    sub_quantity: number,
    sub_unit: string
}
