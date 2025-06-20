
export default function SimpleNavbar() {
    return (
        <div className="navbar bg-primary w-full">
            <div className="flex flex-row mx-2 flex-1 px-2 gap-2 ml-20">
                <img src="/images/nashtech.png" alt="logo" className="w-8 h-8" />
                <span className="text-primary-content text-2xl font-bold">Online Asset Management</span>
            </div>
        </div>
    );
}
