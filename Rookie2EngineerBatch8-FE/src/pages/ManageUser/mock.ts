import { Gender, Location, Type } from "@/types/enums";
import { PaginatedResponse } from "@/types/meta";
import { UserDetail } from "@/types/user";

export const mockRoles = ["Staff", "Admin"];
export const mockUser: UserDetail = {
  staff_code: "SD1901",
  first_name: "Nguyen Van",
  last_name: "A",
  username: "avt",
  join_date: "2015-07-23T14:32:01",
  id: 1,
  date_of_birth: "2015-07-23T14:32:01",
  gender: Gender.MALE,
  location: Location.HANOI,
  type: Type.ADMIN,
};

const mockUserList = Array(20).fill(mockUser)

export const mockUsersResponse: PaginatedResponse<UserDetail[]> = {
  data: mockUserList,
  meta: {
    page: 2,
    pageSize: 20,
    total: 20 * 8,
    total_pages: 8
  }
}
