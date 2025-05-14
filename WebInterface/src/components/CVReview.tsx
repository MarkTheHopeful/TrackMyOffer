import React, { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { UploadIcon, SearchIcon, DownloadIcon, ArrowLeftIcon, PercentIcon } from 'lucide-react';
import { requestCVReview } from '@/api/backend';

export function CVReview() {
    const [file, setFile] = useState<File | null>(null);
    const [jobDescription, setJobDescription] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [matchScore, setMatchScore] = useState<number | null>(null);
    const [isDragging, setIsDragging] = useState(false);
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [suggestions, setSuggestions] = useState<{
        keywords: string[];
        structure: string[];
        ats: string[];
    }>({ keywords: [], structure: [], ats: [] });

    const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            setFile(e.target.files[0]);
        }
    };

    const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = () => {
        setIsDragging(false);
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setFile(e.dataTransfer.files[0]);
        }
    };

    const analyzeCV = async () => {
        // Simulate analysis
        setAnalyzing(true);
        try {
	    const result = await requestCVReview(jobDescription);
	    setMatchScore(result.matchScore);
	    setSuggestions({
                keywords: result.suggestions,
		structure: result.suggestions,
	        ats: result.suggestions,
	    });
	} catch (err) {
             console.error('Error getting a review:', err);
             alert('Failed to get a review. Please check the console for a message.');
        }
        setAnalyzing(false);
    };

    return (
        <div className="w-full max-w-7xl mx-auto">
            <div className="mb-8">
                <h2 className="text-2xl font-semibold text-slate-900 mb-6">CV Review Tool</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Column */}
                    <div className="space-y-6">
                        {/* CV Upload */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Upload Your CV</h3>
                            <div
                                className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer ${isDragging ? 'border-brand-500 bg-brand-50' : 'border-slate-300'
                                    }`}
                                onDragOver={handleDragOver}
                                onDragLeave={handleDragLeave}
                                onDrop={handleDrop}
                                onClick={() => fileInputRef.current?.click()}
                            >
                                <UploadIcon className="mx-auto h-12 w-12 text-slate-400 mb-4" />
                                <p className="text-sm text-slate-600 mb-4">
                                    Drag and drop your CV file or click to browse
                                    <br />
                                    <span className="text-xs text-slate-500">
                                        Supports PDF, DOCX, and TXT formats
                                    </span>
                                </p>
                                <input
                                    type="file"
                                    ref={fileInputRef}
                                    accept=".pdf,.docx,.txt"
                                    className="hidden"
                                    onChange={handleFileChange}
                                />
                                <Button
                                    variant="secondary"
                                    className="cursor-pointer"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        fileInputRef.current?.click();
                                    }}
                                >
                                    Browse Files
                                </Button>
                                {file && (
                                    <p className="mt-4 text-sm text-brand-600 font-medium">
                                        Selected: {file.name}
                                    </p>
                                )}
                            </div>
                        </div>

                        {/* Job Description */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Job Description</h3>
                            <textarea
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                rows={6}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 mb-4"
                                placeholder="Paste job description or enter URL..."
                            />
                            <Button
                                variant="primary"
                                className="w-full"
                                onClick={analyzeCV}
                                disabled={analyzing}
                            >
                                <SearchIcon className="w-4 h-4 mr-2" />
                                {analyzing ? 'Analyzing...' : 'Analyze My CV'}
                            </Button>
                        </div>
                    </div>

                    {/* Right Column */}
                    <div className="space-y-6">
                        {/* Match Score */}
                        {matchScore !== null && (
                            <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                                <h3 className="text-lg font-medium text-slate-900 mb-4">Match Score</h3>
                                <div className="flex items-center justify-center p-4">
                                    <div className="relative w-32 h-32">
                                        <div className="absolute inset-0 flex items-center justify-center">
                                            <PercentIcon className="w-6 h-6 text-brand-600 absolute opacity-20" />
                                            <span className="text-4xl font-bold text-brand-600">{matchScore}</span>
                                        </div>
                                        <svg className="w-full h-full" viewBox="0 0 100 100">
                                            <circle
                                                cx="50"
                                                cy="50"
                                                r="45"
                                                fill="none"
                                                stroke="#f1f5f9"
                                                strokeWidth="10"
                                            />
                                            <circle
                                                cx="50"
                                                cy="50"
                                                r="45"
                                                fill="none"
                                                stroke="#4f46e5"
                                                strokeWidth="10"
                                                strokeDasharray={`${matchScore * 2.83} ${283 - matchScore * 2.83}`}
                                                strokeDashoffset="0"
                                                transform="rotate(-90 50 50)"
                                            />
                                        </svg>
                                    </div>
                                </div>
                                <p className="text-center text-slate-600 mt-2">
                                    {matchScore < 50
                                        ? 'Poor match. Significant improvements needed.'
                                        : matchScore < 75
                                            ? 'Good match. Some improvements recommended.'
                                            : 'Excellent match! Minor tweaks suggested.'}
                                </p>
                            </div>
                        )}

                        {/* Placeholder when no analysis has been run */}
                        {matchScore === null && (
                            <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200 flex items-center justify-center min-h-[200px]">
                                <p className="text-slate-400 text-center">
                                    Upload your CV and enter a job description, then click "Analyze My CV" to see your match score and suggestions
                                </p>
                            </div>
                        )}

                        {/* Suggestions */}
                        {matchScore !== null && (
                            <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                                <h3 className="text-lg font-medium text-slate-900 mb-4">Suggested Improvements</h3>

                                <div className="space-y-4">
                                    <div>
                                        <h4 className="font-medium text-slate-800 mb-2">Missing Keywords</h4>
                                        <ul className="list-disc pl-5 text-slate-600">
                                            {suggestions.keywords.map((item, index) => (
                                                <li key={index}>{item}</li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div>
                                        <h4 className="font-medium text-slate-800 mb-2">Structure & Formatting</h4>
                                        <ul className="list-disc pl-5 text-slate-600">
                                            {suggestions.structure.map((item, index) => (
                                                <li key={index}>{item}</li>
                                            ))}
                                        </ul>
                                    </div>

                                    <div>
                                        <h4 className="font-medium text-slate-800 mb-2">ATS Compatibility</h4>
                                        <ul className="list-disc pl-5 text-slate-600">
                                            {suggestions.ats.map((item, index) => (
                                                <li key={index}>{item}</li>
                                            ))}
                                        </ul>
                                    </div>
                                </div>

                                <div className="mt-6 flex gap-3">
                                    <Button variant="secondary" className="flex-1">
                                        <DownloadIcon className="w-4 h-4 mr-2" />
                                        Download Report
                                    </Button>
                                    <Button variant="secondary" className="flex-1">
                                        <ArrowLeftIcon className="w-4 h-4 mr-2" />
                                        Back to Editor
                                    </Button>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
} 
