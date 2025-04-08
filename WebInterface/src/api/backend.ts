const host = import.meta.env.HOST ?? "localhost";
const port = import.meta.env.PORT ?? "8080";
const API_BASE_URL = `http://${host}:${port}`;

export async function fetchMessage(): Promise<string> {
    const response = await fetch(`${API_BASE_URL}/v0/hello`);
    if (!response.ok) {
        throw new Error("Failed to fetch");
    }
    return response.text();
}
