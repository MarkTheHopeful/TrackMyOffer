export async function fetchMessage(): Promise<string> {
    const response = await fetch("http://localhost:8080/api/hello");
    if (!response.ok) {
        throw new Error("Failed to fetch");
    }
    return response.text();
}
