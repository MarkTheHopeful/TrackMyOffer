import { FetchHelloButton } from "./FetchHelloButton";
import { FetchFeaturesHelloButton } from "./FetchFeaturesHelloButton";

export function ApiDemo() {
    return (
        <div className="space-y-6">
            <div className="border border-slate-200 rounded-xl p-6 bg-white">
                <h2 className="text-xl font-semibold mb-4">Backend Connectivity Demo</h2>
                <div className="space-y-4">
                    <FetchHelloButton />
                    <FetchFeaturesHelloButton />
                </div>
            </div>
        </div>
    );
} 