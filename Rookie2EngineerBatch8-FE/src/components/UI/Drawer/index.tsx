import { menuButtons } from "@/configs/menu";
import DrawerButton from "@/components/UI/Buttons/DrawerButton";
import { MenuButtonType } from "@/types/menuButton";
import { useAuthStore } from "@/stores/authStore";
import { UserType } from "@/types/auth";

export default function Drawer() {
    const { user } = useAuthStore();
    const isAdmin = user.type === UserType.ADMIN;
    return (
        <div className="flex flex-col gap-4">
            <div className="flex items-center gap-2">
                <img src="/images/nashtech.png" alt="Nashtech Logo" className="w-10 h-10" />
                <span className="text-lg text-primary font-bold">Online Asset Management</span>
            </div>
            <div className="divider" />
            <div className="join join-vertical">
                {menuButtons.map(
                    (menuButton) =>
                        (menuButton.type === MenuButtonType.PUBLIC || isAdmin) && (
                            <DrawerButton key={menuButton.name} path={menuButton.path} label={menuButton.name} />
                        )
                )}
            </div>
        </div>
    );
}
