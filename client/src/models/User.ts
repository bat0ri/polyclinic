export interface User {
    id: string;
    username: string | null;
    hash_password: string;
    email: string;
    is_active: boolean;
    phone_number: string | null;
    first_name: string | null;
    last_name: string | null;
    create_date: string | null;
    update_date: string | null;
    roles: string[] | null;
}