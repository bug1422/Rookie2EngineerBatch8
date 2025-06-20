import { Menu, ChevronDown, LogOut, UserLock } from "lucide-react";
import Breadcrumbs from "@/components/UI/Breadcrumbs";
import Drawer from "@/components/UI/Drawer";
import { useState } from "react";
import { useAuthStore } from "@/stores/authStore";
import ChangePasswordModal from "../Modal/ChangePasswordModal";
import { LogOutModal } from "@/components/UI/Modal/LogOutModal";

interface NavbarProps {
  children: React.ReactNode;
}

export default function Navbar({ children }: NavbarProps) {
  const { user } = useAuthStore();
  const userName = user.username;
  const [isLogoutModalOpen, setIsLogoutModalOpen] = useState(false);
  const [isChangePasswordOpen, setChangePasswordOpen] = useState(false);

  return (
    <div className="drawer">
      <input id="my-drawer-3" type="checkbox" className="drawer-toggle" />
      <div className="drawer-content flex flex-col w-screen">
        {/* Navbar */}
        <div
          id="navbar"
          className="navbar bg-primary text-primary-content w-full"
        >
          <div className="mx-auto w-full md:w-83/96 flex items-center">
            <div className="flex-none lg:hidden">
              <label
                htmlFor="my-drawer-3"
                aria-label="open sidebar"
                className="btn btn-square btn-ghost"
              >
                <Menu />
              </label>
            </div>
            <div className="hidden md:block mx-2 flex-1 px-2">
              <Breadcrumbs />
            </div>
            <div className="md:hidden flex-1" />
            <div className="flex-none">
              <div
                id="user-dropdown"
                className="dropdown dropdown-end dropdown-hover"
              >
                <div
                  id="user-dropdown-label"
                  role="label"
                  tabIndex={0}
                  className="flex items-center gap-2"
                >
                  {userName} <ChevronDown />
                </div>
                <ul
                  id="user-dropdown"
                  tabIndex={0}
                  className="dropdown-content menu bg-base-100 rounded-box z-1 w-48 p-2 shadow-sm text-base-content"
                >
                  <li role="menuitem">
                    <a
                      onClick={() => {
                        setChangePasswordOpen(true);
                      }}
                      className="flex items-center gap-2"
                    >
                      <UserLock className="w-4 h-4" />{" "}
                      <span className="text-sm">Change Password</span>
                    </a>
                  </li>
                  <li role="menuitem">
                    <a
                      onClick={() => {
                        setIsLogoutModalOpen(true);
                      }}
                      className="flex items-center gap-2"
                    >
                      <LogOut className="w-4 h-4" />
                      <span>Logout</span>
                    </a>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
        {/* Page content here */}
        {children}
      </div>
      <div id="sidebar" className="drawer-side">
        <label
          htmlFor="my-drawer-3"
          aria-label="close sidebar"
          className="drawer-overlay"
        ></label>
        <ul className="menu bg-base-200 min-h-full w-80 p-4">
          {/* Sidebar content here */}
          <Drawer />
        </ul>
      </div>
      <LogOutModal
        isOpen={isLogoutModalOpen}
        onClose={() => setIsLogoutModalOpen(false)}
      />
      <ChangePasswordModal
        isOpen={isChangePasswordOpen}
        onClose={() => setChangePasswordOpen(false)}
        modalId="_navbar" // Add unique ID
      />
    </div>
  );
}
