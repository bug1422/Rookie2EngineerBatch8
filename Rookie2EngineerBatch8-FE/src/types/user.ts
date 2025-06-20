import { SortDirection, UserSortOption, Type, Gender, Location} from "./enums";

export interface UserBase {
    id: number;
    // staff_code: string;
    first_name: string;
    last_name: string;
    // username: string;
    gender: Gender;
    date_of_birth: string;
    join_date: string;
    type: Type;
    location: Location;
}
export interface UserDetail extends UserBase{
    staff_code: string;
    username: string;
}

export interface UserUpdate {
    date_of_birth: string;
    join_date: string;
    type: Type;
    gender: Gender;
    location: Location;
}

export interface UserDetail extends UserBase{
    staff_code: string;
    username: string;
}


export interface UserListQueryParams {
  page: number;
  type: Type | null;
  search: string | null;
  sortBy: UserSortOption | null;
  sortDirection: SortDirection | null;
}

export interface UserReadSimple {
    id: number;
    first_name: string;
    last_name: string;
    username: string;
}