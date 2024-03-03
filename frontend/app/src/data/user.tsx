export interface User {
    email: string;
    first_name: string;
    last_name: string;
}

export interface UserPreferences {
    user: string;
    servings_per_meal: number;
    cookings_per_week: number;
}

export const user: User = {
    'email': 'user@example.com',
    'first_name': 'John',
    'last_name': 'Doe'
}

export const userPreferences: UserPreferences = {
    'user': 'user@example.com',
    'servings_per_meal': 3,
    'cookings_per_week': 5
}
