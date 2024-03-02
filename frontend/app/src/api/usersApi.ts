import axios from 'axios';
import { createUserSchema } from './apiSchemas/usersSchemas';
import { baseUrl } from './apiConfig';

const usersUrl: string = baseUrl + 'users/';


export async function createUser(data: createUserSchema): Promise<any> {
        return await axios.post(usersUrl, data)
        .then((response) => {
            console.log(response);
          });
}
