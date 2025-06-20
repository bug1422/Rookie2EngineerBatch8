import { Breadcrumb } from "@/types/breadcrumb";
import { create } from "zustand";

interface BreadcrumbsStore {
    breadcrumbs: Breadcrumb[];
    setBreadcrumbs: (crumbs: Breadcrumb[]) => void;
}

export const useBreadcrumbsStore = create<BreadcrumbsStore>((set) => ({
    breadcrumbs: [],
    setBreadcrumbs: (crumbs) => set({ breadcrumbs: crumbs }),
}));
