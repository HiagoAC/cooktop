import axios from 'axios';
import { createMealPlanSchema } from './apiSchemas/mealPlansSchemas';
import { BASE_URL } from './apiConfig';

const MEAL_PLANS_URL: string = BASE_URL + 'meal-plans/';


export async function createMealPlan(data: createMealPlanSchema): Promise<any> {
    const response = await axios.post(MEAL_PLANS_URL, data);
    console.log(response);
    return response;        
}
