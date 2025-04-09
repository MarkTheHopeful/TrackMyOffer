import { useState } from "react";
import { fetchFeaturesHelloMessage } from "../api/backend";
import { Button } from "./ui/button";

export function FetchFeaturesHelloButton() {
    const [result, setResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        console.log("FetchFeaturesHelloButton handleClick");
        try {
            const msg = await fetchFeaturesHelloMessage();
            console.log("FetchFeaturesHelloButton msg", msg);
            setResult(msg);
            setError(null);
        } catch (e) {
            setError((e as Error).message);
        }
    };

    return (
        <div className="space-y-2">
            <Button onClick={handleClick} variant="secondary">Fetch Features Message</Button>
            {result && <p className="text-slate-700">Response: {result}</p>}
            {error && <p className="text-red-500">{error}</p>}
        </div>
    );
} 