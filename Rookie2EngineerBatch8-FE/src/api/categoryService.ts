import { IsValid } from "@/types/isValid";
import { CategoryCreate, CategoryDetail } from "@/types/category";

import axiosClient from "@api/axiosClient";

const API_BASE_ROUTE = `/v1/categories`;

export const categoryService = {
 
  get_category: (id: number) => {
    return axiosClient.get<CategoryDetail>(`${API_BASE_ROUTE}/${id}`);
  },
  
  create_category: (category: CategoryCreate) => {
    return axiosClient.post<CategoryDetail>(`${API_BASE_ROUTE}`, category);
  },
  check_valid_category: (id: number) => {
    return axiosClient.get<IsValid>(`${API_BASE_ROUTE}/valid-category/${id}`);
  },
  get_category_list: () => {
    return axiosClient.get<CategoryDetail[]>(`${API_BASE_ROUTE}`);
  }
};