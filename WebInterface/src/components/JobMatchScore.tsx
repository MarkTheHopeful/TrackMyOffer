import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { SearchIcon, DownloadIcon, ArrowLeftIcon, PercentIcon } from 'lucide-react';
import { requestMatchScore } from '@/api/backend';

export function JobMatchScore() {
    const [jobDescription, setJobDescription] = useState('');
    const [analyzing, setAnalyzing] = useState(false);
    const [matchScore, setMatchScore] = useState<number | null>(null);
    const [suggestions, setSuggestions] = useState<{
        keywords: string[];
        structure: string[];
        ats: string[];
    }>({ keywords: [], structure: [], ats: [] });

    const getMatchScore = async () => {
        setAnalyzing(true);
        try {
            const result = await requestMatchScore(jobDescription);
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
                <h2 className="text-2xl font-semibold text-slate-900 mb-4">Job Match Score</h2>
                
                {/* New description section */}
                <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200 mb-8">
                    <p className="text-slate-600 text-lg leading-relaxed">
                        Get your job match score based on your profile and the job description. 
                        Simply paste the job description or a link to the position, and we'll analyze 
                        how well your experience and skills match the requirements.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Column */}
                    <div className="space-y-6">
                        {/* Job Description */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Job Description</h3>
                            <textarea
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                rows={10}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 mb-4 resize-none"
                                placeholder="Paste job description or enter URL..."
                            />
                            <Button
                                variant="primary"
                                className="w-full"
                                onClick={getMatchScore}
                                disabled={analyzing}
                            >
                                <SearchIcon className="w-4 h-4 mr-2" />
                                {analyzing ? 'Analyzing...' : 'Get Match Score'}
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
                                    Enter a job description, then click "Get Match Score" to see your match score and suggestions
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
