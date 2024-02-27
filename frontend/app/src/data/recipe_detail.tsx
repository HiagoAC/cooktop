export interface Ingredient {
    name: string;
    quantity: string;
    unit: string;
}

export const recipeTypeLabels: Record<string, string> = {
    'mai': 'Main Dish',
    'sid': 'Side Dish',
    'sal': 'Salad',
    'des': 'Dessert',
    'sna': 'Snack'
};

export interface Recipe {
    id: number;
    title: string;
    time_minutes: number;
    tags: string[];
    image: string;
    directions: string[];
    description: string;
    recipe_type: string;
    notes: string;
    ingredients: Ingredient[];
}


export const recipesDetail: Record<string, Recipe> = {
    "1": 
        {
            "id": 1,
            "title": "Shrimp and Chicken Pancit Canton",
            "time_minutes": 30,
            "tags": ["Sea food", "Chinese"],
            "image": "/images/img_1.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.",
            "recipe_type": "mai",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        },
    "2":
        {
            "id": 2,
            "title": "Crockpot Sausage Tortellini Soup",
            "time_minutes": 20,
            "tags": ["Easy to make", "Soup"],
            "image": "/images/img_2.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo.",
            "recipe_type": "sid",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        },
    "3":
        {
            "id": 3,
            "title": "Tropical Grilled Chicken Breast",
            "time_minutes": 15,
            "tags": ["Grilling", "Summer", "Barbecue"],
            "image": "/images/img_3.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo.",
            "recipe_type": "sal",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        },
    "4": 
        {
            "id": 4,
            "title": "Shrimp and Chicken Pancit Canton",
            "time_minutes": 30,
            "tags": ["Sea food", "Chinese"],
            "image": "/images/img_1.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo.",
            "recipe_type": "mai",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        },
    "5":
        {
            "id": 5,
            "title": "Crockpot Sausage Tortellini Soup",
            "time_minutes": 20,
            "tags": ["Easy to make", "Soup"],
            "image": "/images/img_2.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo.",
            "recipe_type": "mai",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        },
    "6":
        {
            "id": 6,
            "title": "Tropical Grilled Chicken Breast",
            "time_minutes": 15,
            "tags": ["Grilling", "Summer", "Barbecue"],
            "image": "/images/img_3.webp",
            "directions": [
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris efficitur ligula lacus, eu imperdiet erat facilisis sed. Interdum et malesuada fames ac ante ipsum primis in faucibus. Suspendisse id pharetra orci. Duis et scelerisque velit. Nam sed elit iaculis, maximus neque vel, hendrerit diam. Etiam scelerisque in nibh vel tempus. Proin orci velit, scelerisque id faucibus sit amet, accumsan vitae odio. In hac habitasse platea dictumst. Sed mi risus, euismod eu rhoncus non, suscipit nec tellus. Proin magna nulla, porta tempus sollicitudin ut, finibus a enim. Suspendisse a dictum lectus. In hac habitasse platea dictumst. Suspendisse pharetra metus sit amet pharetra hendrerit. Integer in vulputate lacus. Curabitur id purus dui.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis."
            ],
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo.",
            "recipe_type": "mai",
            "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam egestas ut ex non commodo. Maecenas egestas gravida enim vel viverra. Aenean convallis ac sapien et auctor. Donec dignissim vulputate gravida. Quisque cursus sodales convallis. Phasellus non interdum dolor, ac consectetur nibh. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Pellentesque posuere blandit est, in tristique nulla sagittis at. Mauris cursus mi mollis, sodales sapien eu, interdum risus. Nunc suscipit non massa dapibus viverra. Cras faucibus bibendum quam, eu scelerisque leo. Curabitur eleifend quam suscipit accumsan iaculis. Sed tempus tellus eu sagittis venenatis.",
            "ingredients": [
                {"name": "ing 1", "quantity": "5", "unit": "g"},
                {"name": "ing 2", "quantity": "5", "unit": "g"},
                {"name": "ing 3", "quantity": "5", "unit": "g"}
            ]
        }
}
