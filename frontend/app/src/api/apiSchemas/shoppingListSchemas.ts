/**
 * Schemas for the shopping-list API.
 */


export interface createShoppingItemSchema {
    name: string,
    quantity: number,
    unit: string
}

export interface updateShoppingItemSchema {
    id: number,
    name?: string,
    quantity?: number,
    unit?: string
}