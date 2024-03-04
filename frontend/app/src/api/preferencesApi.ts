import axios from 'axios';
import {
    preferencesSchema,
    preferencesPartialSchema
} from './apiSchemas/preferencesSchemas';
import { BASE_URL } from './apiConfig';

const PREFERENCES_URL: string = BASE_URL + 'preferences/';

export async function setPreferences(data: preferencesSchema): Promise<any> {
    const response = await axios.post(PREFERENCES_URL, data);
    console.log(response);
    return response;        
}

export async function getPreferences(): Promise<any> {
    const response = await axios.get(PREFERENCES_URL);
    console.log(response);
    return response;    
}

export async function updatePreferences(
    data: preferencesPartialSchema): Promise<any> {
    const response = await axios.patch(PREFERENCES_URL, data);
    console.log(response);
    return response;        
}
