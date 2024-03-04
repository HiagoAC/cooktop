/**
 * Schemas for the users API.
 */


export interface createUserSchema {
    email: string,
    password: string,
    first_name: string,
    last_name: string
}


export interface userUpdateSchema {
    first_name: string,
    last_name: string
}

export interface changePasswordSchema {
    old_password: string,
    new_password: string
}
