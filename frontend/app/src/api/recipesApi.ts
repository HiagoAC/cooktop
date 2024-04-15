/**
 * Functions for the recipes endpoint.
 */

import axios from 'axios';
import { RecipeIn } from './apiSchemas/recipesSchemas';
import { BASE_URL } from './apiConfig';


const RECIPES_URL: string = BASE_URL + 'recipes/';


export async function createRecipe(data: RecipeIn): Promise<any> {
    const response = await axios.post(RECIPES_URL, data);
    console.log(response);
    return response;        
}

export async function uploadImage(recipeId: string, img: File): Promise<any> {
    const data = new FormData();
    data.append('img', img);
    const response = await axios.post(`${RECIPES_URL}${recipeId}/image`, data);
    console.log(response);
    return response;
}
