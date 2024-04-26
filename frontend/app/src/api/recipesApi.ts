/**
 * Functions for the recipes endpoint.
 */

import axios from 'axios';
import { RecipeIn, RecipePatch } from './apiSchemas/recipesSchemas';
import { BASE_URL } from './apiConfig';


const RECIPES_URL: string = BASE_URL + 'recipes/';


export async function getRecipes(): Promise<any> {
    const response = await axios.get(RECIPES_URL);
    console.log(response);
    return response;
}

export async function createRecipe(data: RecipeIn): Promise<any> {
    const response = await axios.post(RECIPES_URL, data);
    console.log(response);
    return response;
}

export async function downloadImage(recipeId: string): Promise<any> {
    const response = await axios.get(
        `${RECIPES_URL}${recipeId}/image`, { responseType: 'blob' });
    console.log(response);
    return response;
}

export async function uploadImage(recipeId: string, img: File): Promise<any> {
    const data = new FormData();
    console.log('upload Image ' + img.name);
    data.append('img', img);
    const response = await axios.post(`${RECIPES_URL}${recipeId}/image`, data);
    console.log(response);
    return response;
}

export async function getRecipeDetail(recipeId: string): Promise<any> {
    const response = await axios.get(`${RECIPES_URL}${recipeId}`);
    console.log(response);
    return response;
}

export async function updateRecipe(recipeId: string, data: RecipePatch): Promise<any> {
    const response = await axios.patch(`${RECIPES_URL}${recipeId}`, data);
    console.log(response);
    return response;
}
