import { useState } from "react";
import { Button } from "./ui/button";
import {authentify, fetchHelloMessage} from "@/api/backend.ts";

export function LogInButton() {
    const [result, setResult] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);

    const handleClick = async () => {
        try {
            const response = await authentify();
            console.log("LogIn response:", response);
            setResult(response);
            setError(null);
        } catch (error) {
            console.error("Error during login:", error);
            setError((error as Error).message);
        }
    };

    return (
        <div className="space-y-2">
            <button onClick={handleClick} className="bg-blue-500 text-white px-4 py-2 rounded">
                Log In
            </button>
            {result && <p className="text-slate-700">Response: {result}</p>}
            {error && <p className="text-red-500">{error}</p>}
        </div>
    );

    // const [result, setResult] = useState<string | null>(null);
    // const [error, setError] = useState<string | null>(null);
    //
    // const handleClick = async () => {
    //     try {
    //         const msg = await authentify();
    //         setResult(msg);
    //         setError(null);
    //     } catch (e) {
    //         setError((e as Error).message);
    //     }
    // };
    //
    // return (
    //     <div className="space-y-2">
    //         <Button onClick={handleClick} variant="secondary">Fetch Hello Message</Button>
    //         {result && <p className="text-slate-700">Response: {result}</p>}
    //         {error && <p className="text-red-500">{error}</p>}
    //     </div>
    // );
    // const handleClick = async () => {
    //     try {
    //         const response = await fetch("http://localhost:8080/login");
    //         if (!response.ok) {
    //             throw new Error("Failed to fetch: " + response.statusText);
    //         }
    //         const text = await response.text();
    //         console.log("LogIn response:", text);
    //     } catch (error) {
    //         console.error("Error during login:", error);
    //     }
    // };
    //
    // return (
    //     <div className="space-y-2">
    //         <button onClick={handleClick} className="bg-blue-500 text-white px-4 py-2 rounded">
    //             Log In
    //         </button>
    //     </div>
    // );
}