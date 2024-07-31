import axios from 'axios';
import { createMealPlanSchema, updateMealPlanSchema } from './apiSchemas/mealPlansSchemas';
import { BASE_URL } from './apiConfig';

const MEAL_PLANS_URL: string = BASE_URL + 'meal-plans/';
const CURRENT_PLAN_URL: string = MEAL_PLANS_URL + 'current';


export async function createMealPlan(data: createMealPlanSchema): Promise<any> {
    const response = await axios.post(MEAL_PLANS_URL, data);
    console.log(response);
    return response;        
}

export async function getMealPlan(): Promise<any> {
    const response = await axios.get(CURRENT_PLAN_URL);
    console.log(response);
    return response;
}

export async function updateMealPlan(id: number, data: updateMealPlanSchema): Promise<any> {
    const response = await axios.patch(MEAL_PLANS_URL + id, data);
    console.log(response);
    return response;
}


export async function subtractIngredientsFromPantry(id: number): Promise<any> {
    const response = await axios.post(MEAL_PLANS_URL + id + '/subtract-from-pantry');
    console.log(response);
    return response;
}

export async function addIngredientsToShoppingList(id: number): Promise<any> {
    const response = await axios.post(MEAL_PLANS_URL + id + '/add-to-shopping-list');
    console.log(response);
    return response;
}