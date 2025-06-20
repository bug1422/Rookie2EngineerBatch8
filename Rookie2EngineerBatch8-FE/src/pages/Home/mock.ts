// import { MyAssignmentDetail } from "@/types/assignment";
// import { State } from "@/types/enums";
// import { PaginatedResponse } from "@/types/meta";

// export const mockAssignment: MyAssignmentDetail = {
//   id: 1,
//   asset_code: "LA100002",
//   asset_name: "Laptop HP ProBook 450 G5",
//   category: "Laptop",
//   assigned_to: "John Doe",
//   assigned_by: "Jane Smith",
//   specification: "Intel Core i5, 8GB RAM, 256GB SSD",
//   note: "Assigned for project X",
//   assigned_date: "12/10/2018",
//   assignment_state: State.ACCEPTED,
// };

// export const mock2Assignment: MyAssignmentDetail = {
//   id: 2,
//   asset_code: "MO100004",
//   asset_name: "Monitor Dell P2419H",
//   category: "Monitor",
//   assigned_to: "John Doe",
//   assigned_by: "Jane Smith",
//   specification: "24-inch, Full HD, IPS",
//   note: "Assigned for project X",
//   assigned_date: "12/10/2018",
//   assignment_state: State.WAITING_FOR_ACCEPTANCE,
// };

// const mockAssignmentList = Array(10).fill(mockAssignment);
// const mock2AssignmentList = Array(10).fill(mock2Assignment);

// export const mockMyAssignmentsResponse: PaginatedResponse<MyAssignmentDetail[]> =
//   {
//     data: [...mockAssignmentList, ...mock2AssignmentList],
//     meta: {
//       page: 2,
//       pageSize: 20,
//       total: 20 * 4,
//       total_pages: 4,
//     },
//   };
