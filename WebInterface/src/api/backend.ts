const host = import.meta.env.VITE_API_HOST ?? "localhost";
const port = import.meta.env.VITE_API_PORT ?? "8080";
const API_BASE_URL = `http://${host}:${port}`;

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

export function authentify(): void {
    window.location.href = `${API_BASE_URL}/login`;
}
// export async function authentify(): Promise<string> {
    // const response = await fetch(`${API_BASE_URL}/login`);
    // if (!response.ok) {
    //     throw new Error("Failed to fetch: " + response.statusText);
    // }
    // return response.text();
// }