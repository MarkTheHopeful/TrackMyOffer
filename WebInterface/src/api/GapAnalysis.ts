export interface Gap {
    gap_text: string;
    severity: "Critical" | "Important" | "Nice-to-have";
    suggestion: string;
}

export interface GapAnalysisResult {
    gaps: Gap[];
}
