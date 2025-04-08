import { useState } from "react";
import { fetchFeaturesHelloMessage } from "../api/backend";

export function FetchFeaturesHelloButton() {
    const [result, setResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        try {
            const msg = await fetchFeaturesHelloMessage();
            setResult(msg);
            setError(null);
        } catch (e) {
            setError((e as Error).message);
        }
    };

    return (
        <div>
            <button onClick={handleClick}>Fetch Features Message</button>
            {result && <p>Response: {result}</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
}
