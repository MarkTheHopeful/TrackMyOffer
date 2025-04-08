import { useState } from "react";
import { fetchMessage } from "../api/backend";

export function FetchButton() {
    const [result, setResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        try {
            const msg = await fetchMessage();
            setResult(msg);
            setError(null);
        } catch (e) {
            setError("Something went wrong.");
        }
    };

    return (
        <div>
            <button onClick={handleClick}>Fetch Message</button>
            {result && <p>Response: {result}</p>}
            {error && <p style={{ color: "red" }}>{error}</p>}
        </div>
    );
}
