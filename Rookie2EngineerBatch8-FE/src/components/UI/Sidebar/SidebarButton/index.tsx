import { MenuButton } from "@/types/menuButton";
import { Link, useLocation } from "react-router-dom";

export default function SidebarButton({ name, path }: MenuButton) {
    const location = useLocation();
    const getFirstSegment = (location: string) => location.split('/')[1] || '';
    const isActive = getFirstSegment(location.pathname) === getFirstSegment(path);
    return (
        <Link
            id="sidebar-button"
            to={path}
            className={`h-12 btn join-item justify-start w-full font-bold text-lg ${isActive ? "btn-primary" : ""}`}
        >
            {name}
        </Link>
    );
}
