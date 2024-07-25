import axios from 'axios';
import {
    createShoppingItemSchema,
    updateShoppingItemSchema
} from './apiSchemas/shoppingListSchemas';
import { BASE_URL } from './apiConfig';

const SHOPPING_LIST_URL: string = BASE_URL + 'shopping-list/';
const CLEAR_SHOPPING_LIST_URL: string = SHOPPING_LIST_URL + 'clear-list';
const ADD_TO_PANTRY_URL: string = SHOPPING_LIST_URL + 'add-list-to-pantry';

export async function addItemToList(data: createShoppingItemSchema): Promise<any> {
    console.log(data)
    const response = await axios.post(SHOPPING_LIST_URL, data);
    console.log(response);
    return response;        
}

export async function getShoppingList(): Promise<any> {
    const response = await axios.get(SHOPPING_LIST_URL);
    console.log(response);
    return response;
}

export async function updateShoppingItem(data: updateShoppingItemSchema): Promise<any> {
    const response = await axios.patch(`${SHOPPING_LIST_URL}${data.id}`, data);
    console.log(response);
    return response;
}

export async function deleteShoppingItem(id: number): Promise<any> {
    const response = await axios.delete(`${SHOPPING_LIST_URL}${id}`);
    console.log(response);
    return response;
}

export async function clearList(): Promise<any> {
    const response = await axios.delete(CLEAR_SHOPPING_LIST_URL);
    console.log(response);
    return response;
}

export async function addShoppingItemsToPantry(): Promise<any> {
    const response = await axios.post(ADD_TO_PANTRY_URL);
    console.log(response);
    return response;
}