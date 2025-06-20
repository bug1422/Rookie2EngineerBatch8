export interface CategoryCreate {
    category_name: string;
    prefix: string; // Optional field
    // Add other fields necessary for creating a category
  }

export interface CategoryDetail {
    id: number;
    category_name: string;
    prefix: string;
    // Add other fields as necessary
}