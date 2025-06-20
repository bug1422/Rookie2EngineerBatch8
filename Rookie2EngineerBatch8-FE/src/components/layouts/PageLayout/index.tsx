interface PageLayoutProps {
    children: React.ReactNode;
    title: string;
}

export default function PageLayout({ children, title }: PageLayoutProps) {
    return (
        <div className="flex flex-col mx-auto w-full">
            <h1 className="text-xl font-bold text-primary">{title}</h1>
            <div className="flex-1 mt-4">
                {children}
            </div>
        </div>
    )
}

