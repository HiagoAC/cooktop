import axios from 'axios';
import {
    ShoppingListItem
} from './apiSchemas/shoppingListSchemas';
import { BASE_URL } from './apiConfig';

const SHOPPING_LIST_URL: string = BASE_URL + 'shopping-list/';

export async function addItemToList(data: ShoppingListItem): Promise<any> {
    const response = await axios.post(SHOPPING_LIST_URL, data);
    console.log(response);
    return response;        
}
