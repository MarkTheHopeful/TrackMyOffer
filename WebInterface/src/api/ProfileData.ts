import { EducationEntry } from "./EducationEntry.ts";

export interface ProfileData {
  first_name?: string;
  last_name?: string;
  email?: string;
  phone?: string;
  city?: string;
  state?: string;
  country?: string;
  education?: EducationEntry[];
  linkedin_url?: string;
  github_url?: string;
  personal_website?: string;
  other_url?: string;
  about_me?: string;
  [key: string]: string | EducationEntry[] | undefined;
}
