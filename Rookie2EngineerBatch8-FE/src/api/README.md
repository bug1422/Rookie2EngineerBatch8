# API Folder

This folder contains API-related utilities and modules for the project.

## Structure

-   **axiosClient.ts**: The base Axios instance configured for making HTTP requests throughout the application. It handles base URL, interceptors, and common settings.
-   **<_serviceName_>.ts**: Service modules that define functions for making API calls related to specific resources or features. Each service module typically imports the `axiosClient` instance and defines functions for CRUD operations.

## Usage

Import `axiosClient` in your services or components to perform API calls:

``` js
// authorService.ts
import axiosClient from "@api/axiosClient";
import { Author } from "@/types/author";

const API_BASE_ROUTE = "/api/v1/authors";
export const authorService = {
    getAuthors: () => axiosClient.get<Author[]>(`${API_BASE_ROUTE}`),
};
```