export interface ShoppingItem {
    id: string;
    name: string;
    quantity: string;
    unit: string;
}


export const shoppingList: ShoppingItem[] = [
    {
        "id": "1",
        "name": "ing 1",
        "quantity": "3",
        "unit": "cup",
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
    },
    {
        "id": "4",
        "name": "ing 4",
        "quantity": "500",
        "unit": "g",
    }
]
