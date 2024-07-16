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

export async function updatePantryItem(data: createPantryItemSchema): Promise<any> {
    const response = await axios.patch(`${PANTRY_URL}${data.id}`, data);
    console.log(response);
    return response;
}

export async function deletePantryItem(id: number): Promise<any> {
    const response = await axios.delete(PANTRY_URL + id);
    console.log(response);
    return response;
}
