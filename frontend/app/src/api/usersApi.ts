import axios from 'axios';
import { createUserSchema } from './apiSchemas/usersSchemas';
import { BASE_URL } from './apiConfig';

const USERS_URL: string = BASE_URL + 'users/';
const ME_URL: string = USERS_URL + 'me';

export async function createUser(data: createUserSchema): Promise<any> {
    const response = await axios.post(USERS_URL, data);
    console.log(response);
    return response;        
}

export async function getUser(): Promise<any> {
    const response = await axios.get(ME_URL);
    console.log(response);
    return response;    
}
