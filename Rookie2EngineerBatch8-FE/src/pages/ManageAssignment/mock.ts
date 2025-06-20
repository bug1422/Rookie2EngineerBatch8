// import { AssignmentDetail } from "@/types/assignment";
// import { AssignmentState} from "@/types/enums";
// import { PaginatedResponse } from "@/types/meta";

// export const mockAssignment: AssignmentDetail = {
//   id: 1,
//   asset_code: "PC100115",
//   asset_name: "Laptop HP ProBook 450 G5",
//   specification: "Intel Core i5-8250U, 8GB RAM, 256GB SSD",
//   assigned_to_username: "hungtv1",
//   assigned_by_username: "binhnv",
//   assign_date: "12/10/2018",
//   assignment_state: AssignmentState.ACCEPTED,
//   assignment_note: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
// };

// export const mock2Assignment: AssignmentDetail = {
//   id: 21,
//   asset_code: "PC100115",
//   asset_name: "Laptop HP ProBook 450 G5",
//   specification: "Intel Core i5-8250U, 8GB RAM, 256GB SSD",
//   assigned_to_username: "hungtv1",
//   assigned_by_username: "binhnv",
//   assign_date: "12/10/2018",
//   assignment_state: AssignmentState.WAITING_FOR_ACCEPTANCE,
//   assignment_note: "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
// };

// const mockAssignmentList = Array(10).fill(mockAssignment)
// const mock2AssignmentList = Array(10).fill(mock2Assignment);

// export const mockAssignmentsResponse: PaginatedResponse<AssignmentDetail[]> = {
//   data: [
//     ...mockAssignmentList,
//     ...mock2AssignmentList
//   ],
//   meta: {
//     page: 2,
//     pageSize: 20,
//     total: 20 * 8,
//     total_pages: 8
//   }
// }
