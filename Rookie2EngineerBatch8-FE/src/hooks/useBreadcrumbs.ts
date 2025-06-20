import { useEffect } from "react";
import { Breadcrumb } from "@/types/breadcrumb";
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";

export function useBreadcrumbs(crumbs: Breadcrumb[]) {
    const setBreadcrumbs = useBreadcrumbsStore((state) => state.setBreadcrumbs);
    useEffect(() => {
        setBreadcrumbs(crumbs);
    }, [crumbs, setBreadcrumbs]);
}
