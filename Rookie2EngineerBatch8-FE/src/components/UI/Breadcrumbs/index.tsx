import { ChevronRight } from "lucide-react";
import { useBreadcrumbsStore } from "@/stores/breadcrumbs";

export default function Breadcrumbs() {
    const breadcrumbs = useBreadcrumbsStore((state) => state.breadcrumbs);

    if (breadcrumbs.length === 0) return null;

    return (
        <nav className="text-xl font-bold" aria-label="Breadcrumb">
            <ol className="flex items-center">
                {breadcrumbs.map((crumb, idx) => {
                    const isLast = idx === breadcrumbs.length - 1;
                    return (
                        <li key={idx} className="flex items-center">
                            {idx > 0 && <ChevronRight className="mx-2" strokeWidth={3} size={20} />}
                            {crumb.path && !isLast ? (
                                <a href={crumb.path} className="hover:underline">
                                    {crumb.label}
                                </a>
                            ) : (
                                <span>{crumb.label}</span>
                            )}
                        </li>
                    );
                })}
            </ol>
        </nav>
    );
}
