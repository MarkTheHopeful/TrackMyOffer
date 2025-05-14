export interface Experience {
    id: number;
    profile_id: number;
    job_title: string;
    company: string;
    start_date: string;
    end_date: string | null;
    description: string | null;
} 