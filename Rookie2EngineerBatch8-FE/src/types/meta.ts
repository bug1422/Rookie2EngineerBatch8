export interface PaginationMeta{
    total: number,
    total_pages: number,
    page: number,
    pageSize: number
}
export interface PaginatedResponse<T>{
    data: T,
    meta: PaginationMeta
}