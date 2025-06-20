import { Link, useLocation } from "react-router-dom";

interface DrawerButtonProps {
    path: string;
    label: string;
}

export default function DrawerButton({ path, label }: DrawerButtonProps) {
    const location = useLocation();
    const getFirstSegment = (location: string) => location.split("/")[1] || "";
    const isActive = getFirstSegment(location.pathname) === getFirstSegment(path);
    return (
        <div className="h-10/12 w-full">
            <Link
                to={path}
                className={`
                    btn w-full justify-start border-none
                    ${isActive ? "btn-primary" : ""}
                `}
            >
                <div className="flex items-center gap-2 overflow-hidden">
                    <span className="whitespace-nowrap">{label}</span>
                </div>
            </Link>
        </div>
    );
}
