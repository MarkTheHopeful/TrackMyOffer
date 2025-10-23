import {ProfileData} from "@/api/ProfileData.ts";
import {EducationEntry} from "@/api/EducationEntry.ts";
import {Experience} from "@/api/Experience.ts";

export interface ExportResponse {
    profile?: ProfileData;
    education: EducationEntry[];
    experience: Experience[];
}