import { LogInButton } from "./LogInButton";

export function LogIn() {
    return (
        <div className="space-y-6">
            <div className="border border-slate-200 rounded-xl p-6 bg-white">
                <h2 className="text-xl font-semibold mb-4">Login Demo</h2>
                <div className="space-y-4">
                    <LogInButton />
                </div>
            </div>
        </div>
    );
}