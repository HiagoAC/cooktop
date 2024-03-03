/**
 * Schemas for the tokens API.
 */

export interface Tokens {
    access_token: string;
    refresh_token: string;
}

export interface getTokensSchema {
    email: string,
    password: string
}
