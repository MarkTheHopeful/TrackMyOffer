import { UserContract } from "./UserContract.ts";

const host = import.meta.env.VITE_API_HOST ?? "localhost";
const port = import.meta.env.VITE_API_PORT ?? "8080";
const fullUrl = import.meta.env.VITE_FULL_API_URL;
const API_BASE_URL = fullUrl
    ? fullUrl
    : `http://${host}:${port}`;

export async function fetchHelloMessage(): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/v0/hello`);
    if (!response.ok) {
        throw new Error("Failed to fetch: " + response.statusText);
    }
    return response.text();
}

export async function fetchFeaturesHelloMessage(): Promise<string> {
    const url = `${API_BASE_URL}/features/v0/hello?name=aboba`;
    console.log("fetchFeaturesHelloMessage", url);
    const response = await fetch(url);
    console.log("fetchFeaturesHelloMessage response", response);
    if (!response.ok) {
        throw new Error("Failed to fetch: " + response.statusText);
    }
    return response.text();
}

export async function authentify(): Promise<string | null> {
    window.location.href = `${API_BASE_URL}/login`;
    return null;
}

export async function checkAuthStatus(): Promise<{ authenticated: boolean; user?: UserContract }> {
    const response = await fetch(`${API_BASE_URL}/auth/status`, {
        method: 'GET',
        headers: {
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
        credentials: "include",
        mode: "cors"
    });
    console.log("Auth status response:", response);
    if (response.ok) {
        const data = await response.json();
        return {
            authenticated: data.isAuthenticated,
            user: data.userData ? {
                id: data.userData.id,
                username: data.userData.name,
                firstName: data.userData.givenName,
                email: data.userData.email,
                picture: data.userData.picture
            } as UserContract : undefined,
        };
    }
    return { authenticated: false };
}

export async function logout(): Promise<void> {
    try {
        const response = await fetch(`${API_BASE_URL}/logout`, {
            method: "POST",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
            credentials: "include",
        });

        if (!response.ok) {
            console.error("Logout failed:", response.status, response.statusText);
            // Still redirect to home page even if logout fails
            window.location.href = '/';
            return;
        }

        const data = await response.json();
        console.log("Logout response:", data);

        // Redirect to home page
        window.location.href = '/';
    } catch (error) {
        console.error("Logout error:", error);
        // Still redirect to home page even if there's an error
        window.location.href = '/';
    }
}

interface GenerateCoverLetterRequest {
    jobDescription: string;
    motivations: string;
    tone: 'formal' | 'enthusiastic' | 'creative';
}

export async function generateCoverLetter(request: GenerateCoverLetterRequest): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/features/v0/cover-letter`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(request),
        credentials: 'include'
    });

    if (!response.ok) {
        throw new Error("Failed to generate cover letter: " + response.statusText);
    }

    const data = await response.json();
    return data.content;
}