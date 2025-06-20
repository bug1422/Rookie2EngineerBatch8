import "./App.css";
import { Routes, Route } from "react-router-dom";
import Home from "@/pages/Home";
import ManageUser from "@/pages/ManageUser";
import ManageAsset from "@/pages/ManageAsset";
import ManageAssignment from "@/pages/ManageAssignment";
import RequestForReturning from "@/pages/ManageRequestForReturning";
import Report from "@/pages/Report";
import Login from "@/pages/Login";
import AppLayout from "@components/layouts/AppLayout";
import NotFound from "./pages/NotFound";
import EditUser from "./pages/EditUser";
import CreateUser from "@/pages/CreateUser";
import CreateAsset from "@/pages/CreateAsset";
import ProtectedRoutes from "@/utils/Routes/ProtectedRoutes";
import ChangedPasswordRoutes from "@/utils/Routes/ChangedPasswordRoutes";
import PublicOnlyRoutes from "@/utils/Routes/PublicOnlyRoutes";
import EditAssignment from "./pages/EditAssignment";
import EditAsset from "./pages/EditAsset";
import CreateAssignment from "./pages/CreateAssignment";
import { AdminOnlyRoute } from "./utils/Routes/AdminOnlyRoute";

function App() {
    return (
        <Routes>
            {/* Public routes */}
            <Route element={<PublicOnlyRoutes />}>
                <Route path="/login" element={<Login />} />
            </Route>

            {/* Protected routes */}
            <Route element={<ProtectedRoutes />}>
                {/* All protected routes now go through ChangedPasswordRoutes */}
                <Route element={<ChangedPasswordRoutes />}>
                    <Route element={<AppLayout />}>
                        <Route path="/" element={<Home />} />
                        <Route path="/request-for-returning" element={<RequestForReturning />} />
                        <Route element={<AdminOnlyRoute />}>
                            <Route path="/manage-user" element={<ManageUser />} />
                            <Route path="/manage-user/:id" element={<EditUser />} />
                            <Route path="/manage-user/create-user" element={<CreateUser />} />
                            <Route path="/manage-asset" element={<ManageAsset />} />
                            <Route path="/manage-asset/:id" element={<EditAsset />} />
                            <Route path="/manage-asset/create-asset" element={<CreateAsset />} />
                            <Route path="/manage-assignment" element={<ManageAssignment />} />
                            <Route path="/manage-assignment/create-assignment" element={<CreateAssignment />} />
                            <Route path="/manage-assignment/:id" element={<EditAssignment />} />
                            <Route path="/report" element={<Report />} />
                        </Route>
                    </Route>
                </Route>
            </Route>
            {/* 404 route - must be last */}
            <Route path="*" element={<NotFound />} />
        </Routes>
    );
}

export default App;
