export interface PantryIngredient {
    id: string;
    name: string;
    quantity: string;
    unit: string;
    expiration?: string
}


export const pantryIngredients: PantryIngredient[] = [
    {
        "id": "1",
        "name": "ing 1",
        "quantity": "3",
        "unit": "cup",
        "expiration": "2024-05-25",
    },
    {
        "id": "2",
        "name": "ing 2",
        "quantity": "10",
        "unit": "unit",
    },
    {
        "id": "3",
        "name": "ing 3",
        "quantity": "1000",
        "unit": "g",
        "expiration": "2024-03-21",
    },
    {
        "id": "4",
        "name": "ing 4",
        "quantity": "500",
        "unit": "g",
        "expiration": "2024-02-21",
    }
]
