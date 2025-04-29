import { useState } from 'react';;
import { logout } from "@/api/backend.ts";

export function LogOutButton() {
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        try {
            logout();
            setError(null);
        } catch (error) {
            console.error("Error during login:", error);
            setError((error as Error).message);
        }
    };

    return (
        <div className="space-y-2">
            <button onClick={handleClick} className="bg-blue-500 text-white px-4 py-2 rounded">
                Log Out
            </button>
            {error && <p className="text-red-500">{error}</p>}
        </div>
    );
}