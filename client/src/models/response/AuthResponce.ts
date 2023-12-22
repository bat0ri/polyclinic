import { User } from "../User"

export interface AuthResponce {
    access_token: string
    refresh_token: string
    token_type: string
    user: User
}