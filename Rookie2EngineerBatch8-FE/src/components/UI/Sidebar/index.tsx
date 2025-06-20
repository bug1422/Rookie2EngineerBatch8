import { menuButtons } from "@/configs/menu";
import SidebarButton from "./SidebarButton";
import { MenuButtonType } from "@/types/menuButton";
import { useAuthStore } from "@/stores/authStore";
import { UserType } from "@/types/auth";

export default function Sidebar() {
    const { user } = useAuthStore();
    const isAdmin = user.type === UserType.ADMIN;
    return (
        <div id="sidebar">
            <div className="flex flex-col mb-4">
                <img src="/images/nashtech.png" alt="logo" className="w-20 h-20" />
                <h1 className="text-xl text-primary font-bold">Online Asset Management</h1>
            </div>
            <div id="sidebar-buttons" className="join join-vertical w-full">
                {menuButtons.map(
                    (button) =>
                        (button.type === MenuButtonType.PUBLIC || isAdmin) && (
                            <SidebarButton key={button.path} {...button} />
                        )
                )}
            </div>
        </div>
    );
}
