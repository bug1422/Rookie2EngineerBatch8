export enum Location {
  HANOI = "Hanoi",
  HCM = "Ho Chi Minh",
  DANANG = "Danang",
}

export enum Type {
  ADMIN = "admin",
  STAFF = "staff",
}

export enum Status {
  ACTIVE = "active",
  DISABLED = "disabled",
}

export enum Gender {
  MALE = "male",
  FEMALE = "female",
  BLANK = "",
}

export enum IsFirstLogin {
  TRUE = "true",
  FALSE = "false",
}

export enum UserSortOption {
  STAFF_CODE = "staff_code",
  FIRST_NAME = "first_name",
  JOIN_DATE = "join_date",
  TYPE = "type",
  UPDATED_DATE = "updated_at",
}

export enum SortDirection {
  ASC = "asc",
  DESC = "desc",
  NONE = "none",
}

export enum AssetSortOption {
  ASSET_CODE = "asset_code",
  ASSET_NAME = "asset_name",
  CATEGORY = "category",
  STATE = "state",
  UPDATED_DATE = "updated_at",
}

export enum AssetState{
  AVAILABLE = "Available",
  NOT_AVAILABLE = "Not Available",
  ASSIGNED = "Assigned",
  WAITING_FOR_RECYCLING = "Waiting for Recycling",
  RECYCLED = "Recycled",
}

export enum AssignmentSortOption {
  ID = "id",
  ASSET_CODE = "asset_code",
  ASSET_NAME = "asset_name",
  ASSIGNED_TO = "assigned_to",
  ASSIGNED_BY = "assigned_by",
  ASSIGNED_DATE = "assign_date",
  STATE = "state",
  UPDATED_AT = "updated_at",
}

export enum AssignmentState {
  ACCEPTED = "Accepted",
  WAITING_FOR_ACCEPTANCE = "Waiting for acceptance",
  DECLINED = "Declined",
}

export enum MyAssignmentSortOption {
  ASSET_CODE = "asset_code",
  ASSET_NAME = "asset_name",
  CATEGORY = "category",
  ASSIGNED_DATE = "assign_date",
  STATE = "state",
}

export enum ReportSortOption {
  CATEGORY = "category",
  TOTAL = "total",
  ASSIGNED = "assigned",
  AVAILABLE = "available",
  NOT_AVAILABLE = "not_available",
  WAITING_FOR_RECYCLING = "waiting_for_recycling",
  RECYCLED = "recycled",
}

export enum ReturnRequestSortOption {
  ID = "id",
  ASSET_CODE = "asset_code",
  ASSET_NAME = "asset_name",
  REQUESTED_BY = "requested_by",
  ASSIGN_DATE = "assign_date",
  ACCEPTED_BY = "accepted_by",
  RETURN_DATE = "return_date",
  STATE = "state",
}

export enum RequestState {
  COMPLETED = "Completed",
  WAITING_FOR_RETURNING = "Waiting for returning"
}
export enum AssignmentActionType {
  ACCEPT = "accept assignment",
  DECLINE = "decline assignment",
  DELETE = "delete assignment",
  RETURN_REQUEST = "returning request",
}
