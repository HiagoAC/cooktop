import axios from 'axios';
import {
    changePasswordSchema,
    createUserSchema,
    userUpdateSchema
} from './apiSchemas/usersSchemas';
import { BASE_URL } from './apiConfig';

const USERS_URL: string = BASE_URL + 'users/';
const ME_URL: string = USERS_URL + 'me';
const CHANGE_PASSWORD_URL: string = ME_URL + '/change_password/';

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

export async function updateUser(data: userUpdateSchema): Promise<any> {
    const response = await axios.patch(ME_URL, data);
    console.log(response);
    return response;    
}

export async function changePassword(data: changePasswordSchema): Promise<any> {
    try {
        const response = await axios.patch(CHANGE_PASSWORD_URL, data);
        console.log(response);
        return response;
    } catch (error) {
        console.error("Error changing password:", error);
        throw error;
    } 
}
