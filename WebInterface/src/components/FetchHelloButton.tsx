import { useState } from "react";
import { fetchHelloMessage } from "../api/backend";

export function FetchHelloButton() {
    const [result, setResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        try {
            const msg = await fetchHelloMessage();
            setResult(msg);
            setError(null);
        } catch (e) {
            setError((e as Error).message);
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
