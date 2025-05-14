import { UserContract } from "./UserContract.ts";
import { ProfileData } from "./ProfileData.ts";
import { EducationEntry } from "./EducationEntry.ts";
import { Experience } from "./Experience.ts";

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

// export async function fetchProfileInfo(): Promise<ProfileData> {
//     const controller = new AbortController();
//     const timeout = setTimeout(() => controller.abort(), 5_000);
//     try {
//         const res = await fetch(`${API_BASE_URL}/features/v0/profile`, {
//             headers: { 'Accept': 'application/json' },
//             signal: controller.signal,
//             credentials: "include",
//         });
//         clearTimeout(timeout);
//         if (!res.ok) throw new Error(`HTTP ${res.status}`);
//         return await res.json();
//     } catch (err) {
//         clearTimeout(timeout);
//         console.warn('fetchProfileInfo failed, falling back to mock:', err);
//         return {
//             first_name: "Akaky",
//             last_name: "Akakievich",
//             email: "abc@xyz.com",
//             city: "Saint Petersburg",
//             education: [],
//             linkedin_url: "",
//             github_url: "",
//             personal_website: "",
//             other_url: "",
//             about_me: ""
//         };
//     }
// }

// export async function updateProfileInfo(data: ProfileData): Promise<void> {
//     const controller = new AbortController();
//     const timeout = setTimeout(() => controller.abort(), 5_000);
//     try {
//         const res = await fetch(`${API_BASE_URL}/features/v0/profile`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//                 'Accept': 'application/json'
//             },
//             credentials: "include",
//             body: JSON.stringify(data),
//             signal: controller.signal,
//         });
//         clearTimeout(timeout);
//         if (!res.ok) throw new Error(`HTTP ${res.status}`);
//     } catch (err) {
//         clearTimeout(timeout);
//         if ((err as any).name === 'AbortError') {
//             throw new Error('Request timed out');
//         }
//         throw err;
//     }
// }

export async function createEducationEntry(education: Omit<EducationEntry, 'id'>): Promise<EducationEntry> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/education`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(education),
    });
    if (!response.ok) {
        throw new Error(`Failed to create education entry: ${response.statusText}`);
    }
    return response.json();
}

export async function deleteEducationEntry(educationId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/education?educationId=${educationId}`, {
        method: 'DELETE',
        credentials: 'include',
    });
    if (!response.ok) {
        throw new Error(`Failed to delete education entry: ${response.statusText}`);
    }
}

export async function saveProfileData(profileData: Omit<ProfileData, 'education'>): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(profileData),
    });
    if (!response.ok) {
        throw new Error(`Failed to save profile: ${response.statusText}`);
    }
}

export async function getExperiences(): Promise<Experience[]> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/experience`, {
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`Failed to fetch experiences: ${response.statusText}`);
    }
    return response.json();
}

export async function createExperience(experience: Omit<Experience, 'id' | 'profile_id'>): Promise<Experience> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/experience`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(experience),
    });
    if (!response.ok) {
        throw new Error(`Failed to create experience: ${response.statusText}`);
    }
    return response.json();
}

export async function deleteExperience(experienceId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/experience?experienceId=${experienceId}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`Failed to delete experience: ${response.statusText}`);
    }
}

export async function getProfile(): Promise<ProfileData> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile`, {
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`Failed to fetch profile: ${response.statusText}`);
    }
    return response.json();
}

export async function updateProfile(profile: ProfileData): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(profile),
    });
    if (!response.ok) {
        throw new Error(`Failed to update profile: ${response.statusText}`);
    }
}

export async function getEducation(): Promise<EducationEntry[]> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/education`, {
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`Failed to fetch education: ${response.statusText}`);
    }
    return response.json();
}

export async function createEducation(education: Omit<EducationEntry, 'id'>): Promise<EducationEntry> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/education`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(education),
    });
    if (!response.ok) {
        throw new Error(`Failed to create education: ${response.statusText}`);
    }
    return response.json();
}

export async function deleteEducation(educationId: number): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/features/v0/profile/education?educationId=${educationId}`, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'Accept': 'application/json',
        },
    });
    if (!response.ok) {
        throw new Error(`Failed to delete education: ${response.statusText}`);
    }
}
