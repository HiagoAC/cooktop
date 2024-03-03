import axios from 'axios'
import { getTokensSchema, Tokens } from './apiSchemas/tokensSchemas';
import { BASE_URL } from './apiConfig';

const tokensUrl: string = BASE_URL + 'tokens/';


export async function getTokens(data: getTokensSchema): Promise<Tokens> {
    const response = await axios.post(tokensUrl, data);
	return response.data;
}
