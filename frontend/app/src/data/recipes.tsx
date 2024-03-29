export interface RecipeListInfo {
    id: number;
    title: string;
    time_minutes: number;
    tags: string[];
    image: string;
}

export const recipes: RecipeListInfo[] = [
    {
        "id": 1,
        "title": "Shrimp and Chicken Pancit Canton",
        "time_minutes": 30,
        "tags": ["Sea food", "Chinese"],
        "image": "/images/img_1.webp"
    },
    {
        "id": 2,
        "title": "Crockpot Sausage Tortellini Soup",
        "time_minutes": 20,
        "tags": ["Easy to make", "Soup"],
        "image": "/images/img_2.webp"
    },
    {
        "id": 3,
        "title": "Tropical Grilled Chicken Breast",
        "time_minutes": 15,
        "tags": ["Grilling", "Summer", "Barbecue"],
        "image": "/images/img_3.webp"
    },
    {
        "id": 4,
        "title": "Shrimp and Chicken Pancit Canton",
        "time_minutes": 30,
        "tags": ["Sea food", "Chinese"],
        "image": "/images/img_4.webp"
    },
    {
        "id": 5,
        "title": "Crockpot Sausage Tortellini Soup",
        "time_minutes": 20,
        "tags": ["Easy to make", "Soup"],
        "image": "/images/img_5.webp"
    },
    {
        "id": 6,
        "title": "Tropical Grilled Chicken Breast",
        "time_minutes": 15,
        "tags": ["Grilling", "Summer", "Barbecue"],
        "image": "/images/img_6.webp"
    }
]
