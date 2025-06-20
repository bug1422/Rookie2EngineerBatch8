import Navbar from "@/components/UI/Navbar";
import Sidebar from "@/components/UI/Sidebar";
import { Outlet } from "react-router-dom";

export default function AppLayout() {
    return (
        <main className="min-h-screen w-full">
            <Navbar>
                <div className="flex mx-auto w-full md:w-10/12 mt-8">
                    <div className="hidden lg:flex w-1/4">
                        <Sidebar />
                    </div>
                    <div className="flex-1 md:mt-12 w-3/4">
                        <Outlet />
                    </div>
                </div>
            </Navbar>
        </main>
    );
}
