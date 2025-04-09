import React, { useState } from 'react';
import { Button } from '@/components/ui/button';
import { FileTextIcon, CopyIcon, DownloadIcon, RefreshCcwIcon } from 'lucide-react';

type ToneType = 'formal' | 'enthusiastic' | 'creative';

export function CoverLetter() {
    const [jobDescription, setJobDescription] = useState('');
    const [motivations, setMotivations] = useState('');
    const [tone, setTone] = useState<ToneType>('formal');
    const [generatedLetter, setGeneratedLetter] = useState('');
    const [generating, setGenerating] = useState(false);

    const generateLetter = () => {
        setGenerating(true);
        // Simulate letter generation
        setTimeout(() => {
            const letterIntros = {
                formal: "Dear Hiring Manager,\n\nI am writing to express my interest in the position of Software Engineer as advertised. With my background in computer science and extensive experience in web development, I believe I am well-suited for this role.",
                enthusiastic: "Hello Awesome Team!\n\nI'm incredibly excited to apply for the Software Engineer position at your innovative company! As someone who's passionate about creating amazing digital experiences and solving complex problems, I can't wait to bring my skills and energy to your team.",
                creative: "Picture this: Your search for the perfect Software Engineer ends as you discover a candidate who blends technical expertise with creative problem-solving and a passion for user-centered design. That candidate is me, and I'm thrilled to introduce myself."
            };

            const letterBody = `\n\nMy experience includes:\n• Developing and maintaining full-stack web applications using modern technologies\n• Collaborating with cross-functional teams to deliver high-quality software\n• Implementing efficient and scalable solutions to complex technical challenges\n\n${motivations}\n\nBased on the job description, I am particularly interested in contributing to your team's work on innovative solutions that impact real users.`;

            const letterClosings = {
                formal: "\n\nThank you for considering my application. I look forward to the opportunity to discuss how my skills and experience align with your needs.\n\nSincerely,\n[Your Name]",
                enthusiastic: "\n\nI'm super eager to chat more about how I can contribute to your amazing team! Please feel free to reach out any time.\n\nWith enthusiasm,\n[Your Name]",
                creative: "\n\nLet's create something extraordinary together. I'm ready to bring my unique perspective and technical skills to your team's next chapter of innovation.\n\nCreatively yours,\n[Your Name]"
            };

            setGeneratedLetter(`${letterIntros[tone]}${letterBody}${letterClosings[tone]}`);
            setGenerating(false);
        }, 2000);
    };

    const copyToClipboard = () => {
        navigator.clipboard.writeText(generatedLetter);
    };

    const regenerateWithTone = (newTone: ToneType) => {
        setTone(newTone);
        if (generatedLetter) {
            generateLetter();
        }
    };

    return (
        <div className="w-full max-w-7xl mx-auto">
            <div className="mb-8">
                <h2 className="text-2xl font-semibold text-slate-900 mb-6">Cover Letter Generator</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    {/* Left Column - Inputs */}
                    <div className="space-y-6">
                        {/* Job Description */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Job Description</h3>
                            <textarea
                                value={jobDescription}
                                onChange={(e) => setJobDescription(e.target.value)}
                                rows={6}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 mb-2"
                                placeholder="Paste job description or enter URL..."
                            />
                        </div>

                        {/* Motivation Highlights */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Motivation Highlights</h3>
                            <textarea
                                value={motivations}
                                onChange={(e) => setMotivations(e.target.value)}
                                rows={6}
                                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 mb-2"
                                placeholder="Why are you interested in this position? What excites you about the company?"
                            />
                        </div>

                        {/* Tone Selector */}
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Letter Tone</h3>
                            <div className="grid grid-cols-3 gap-3">
                                <button
                                    onClick={() => setTone('formal')}
                                    className={`py-2 px-3 rounded-lg border ${tone === 'formal'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Formal
                                </button>
                                <button
                                    onClick={() => setTone('enthusiastic')}
                                    className={`py-2 px-3 rounded-lg border ${tone === 'enthusiastic'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Enthusiastic
                                </button>
                                <button
                                    onClick={() => setTone('creative')}
                                    className={`py-2 px-3 rounded-lg border ${tone === 'creative'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Creative
                                </button>
                            </div>

                            <div className="mt-6">
                                <Button
                                    variant="primary"
                                    className="w-full"
                                    onClick={generateLetter}
                                    disabled={!jobDescription || !motivations || generating}
                                >
                                    <FileTextIcon className="w-4 h-4 mr-2" />
                                    {generating ? 'Generating...' : 'Generate Letter'}
                                </Button>
                            </div>
                        </div>
                    </div>

                    {/* Right Column - Preview */}
                    <div>
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200 h-full flex flex-col">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-medium text-slate-900">Letter Preview</h3>
                                {generatedLetter && (
                                    <div className="flex space-x-2">
                                        <button
                                            onClick={copyToClipboard}
                                            className="p-2 hover:bg-slate-100 rounded-lg text-slate-600"
                                            title="Copy to clipboard"
                                        >
                                            <CopyIcon className="w-4 h-4" />
                                        </button>
                                        <button
                                            className="p-2 hover:bg-slate-100 rounded-lg text-slate-600"
                                            title="Download as text file"
                                        >
                                            <DownloadIcon className="w-4 h-4" />
                                        </button>
                                    </div>
                                )}
                            </div>

                            {!generatedLetter ? (
                                <div className="flex-1 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-lg p-6">
                                    <p className="text-slate-400 text-center">
                                        Your generated cover letter will appear here
                                    </p>
                                </div>
                            ) : (
                                <>
                                    <div className="flex-1 overflow-auto">
                                        <textarea
                                            value={generatedLetter}
                                            onChange={(e) => setGeneratedLetter(e.target.value)}
                                            className="w-full h-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 resize-none"
                                            style={{ minHeight: '400px' }}
                                        />
                                    </div>

                                    <div className="mt-4">
                                        <p className="text-sm text-slate-500 mb-3">Not quite right? Try a different tone:</p>
                                        <div className="flex space-x-2">
                                            {(['formal', 'enthusiastic', 'creative'] as ToneType[]).map((toneOption) => (
                                                <Button
                                                    key={toneOption}
                                                    variant={tone === toneOption ? 'primary' : 'secondary'}
                                                    size="sm"
                                                    className="text-xs"
                                                    onClick={() => regenerateWithTone(toneOption)}
                                                    disabled={generating}
                                                >
                                                    <RefreshCcwIcon className="w-3 h-3 mr-1" />
                                                    {toneOption.charAt(0).toUpperCase() + toneOption.slice(1)}
                                                </Button>
                                            ))}
                                        </div>
                                    </div>
                                </>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
} 