import axios from 'axios'
import { getTokensSchema, Tokens } from './apiSchemas/tokensSchemas';
import { baseUrl } from './apiConfig';

const tokensUrl: string = baseUrl + 'tokens/';


export async function getTokens(data: getTokensSchema): Promise<Tokens> {
    const response = await axios.post(tokensUrl, data);
	return response.data;
}
