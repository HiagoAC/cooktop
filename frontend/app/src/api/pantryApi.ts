import axios from 'axios';
import { createPantryItemSchema } from './apiSchemas/pantrySchemas';
import { BASE_URL } from './apiConfig';

const PANTRY_URL: string = BASE_URL + 'pantry/';

export async function addItemToPantry(data: createPantryItemSchema): Promise<any> {
    const response = await axios.post(PANTRY_URL, data);
    console.log(response);
    return response;
}

export async function getPantry(): Promise<any> {
    const response = await axios.get(PANTRY_URL);
    console.log(response);
    return response;
}
