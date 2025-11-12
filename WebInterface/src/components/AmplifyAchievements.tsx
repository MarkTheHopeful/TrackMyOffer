import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Sparkles, CopyIcon, PlusIcon, XIcon } from 'lucide-react';
import { rewriteAchievements } from '@/api/backend';

interface AchievementResult {
    original_achievement: string;
    rewritten_achievement: string;
    style: string;
}

type RewriteStyle = 'professional' | 'concise' | 'impactful' | 'quantitative';

export function AmplifyAchievements() {
    const [achievements, setAchievements] = useState<string[]>(['']);
    const [results, setResults] = useState<AchievementResult[]>([]);
    const [amplifying, setAmplifying] = useState(false);
    const [style, setStyle] = useState<RewriteStyle>('professional');

    const addAchievementField = () => {
        setAchievements([...achievements, '']);
    };

    const removeAchievementField = (index: number) => {
        if (achievements.length > 1) {
            setAchievements(achievements.filter((_, i) => i !== index));
        }
    };

    const updateAchievement = (index: number, value: string) => {
        const updated = [...achievements];
        updated[index] = value;
        setAchievements(updated);
    };

    const amplifyAchievements = async () => {
        const nonEmptyAchievements = achievements.filter(a => a.trim() !== '');
        if (nonEmptyAchievements.length === 0) {
            return;
        }

        setAmplifying(true);
        try {
            const response = await rewriteAchievements({
                achievements: nonEmptyAchievements,
                style
            });
            setResults(response.results);
        } catch (err) {
            console.error('Error amplifying achievements:', err);
        } finally {
            setAmplifying(false);
        }
    };

    const copyAll = () => {
        const allRewritten = results.map(r => r.rewritten_achievement).join('\n');
        navigator.clipboard.writeText(allRewritten);
    };

    const hasNonEmptyAchievements = achievements.some(a => a.trim() !== '');

    return (
        <div className="w-full max-w-7xl mx-auto">
            <div className="mb-8">
                <h2 className="text-2xl font-semibold text-slate-900 mb-6">Amplify Achievements</h2>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <div className="space-y-6">
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-medium text-slate-900">Achievements</h3>
                                <Button
                                    variant="secondary"
                                    size="sm"
                                    onClick={addAchievementField}
                                    className="flex items-center gap-2"
                                >
                                    <PlusIcon className="w-4 h-4" />
                                    Add
                                </Button>
                            </div>
                            <div className="space-y-3">
                                {achievements.map((achievement, index) => (
                                    <div key={index} className="flex gap-2">
                                        <textarea
                                            value={achievement}
                                            onChange={(e) => updateAchievement(index, e.target.value)}
                                            rows={2}
                                            className="flex-1 px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                                            placeholder="Enter an achievement statement..."
                                        />
                                        {achievements.length > 1 && (
                                            <button
                                                onClick={() => removeAchievementField(index)}
                                                className="p-2 text-slate-400 hover:text-slate-600 hover:bg-slate-50 rounded-lg transition-colors"
                                                title="Remove"
                                            >
                                                <XIcon className="w-4 h-4" />
                                            </button>
                                        )}
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <h3 className="text-lg font-medium text-slate-900 mb-4">Writing Style</h3>
                            <div className="flex flex-wrap gap-3">
                                <button
                                    onClick={() => setStyle('professional')}
                                    className={`py-2.5 px-4 rounded-lg border transition-colors ${style === 'professional'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700 font-medium'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Professional
                                </button>
                                <button
                                    onClick={() => setStyle('concise')}
                                    className={`py-2.5 px-4 rounded-lg border transition-colors ${style === 'concise'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700 font-medium'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Concise
                                </button>
                                <button
                                    onClick={() => setStyle('impactful')}
                                    className={`py-2.5 px-4 rounded-lg border transition-colors ${style === 'impactful'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700 font-medium'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Impactful
                                </button>
                                <button
                                    onClick={() => setStyle('quantitative')}
                                    className={`py-2.5 px-4 rounded-lg border transition-colors ${style === 'quantitative'
                                        ? 'bg-brand-50 border-brand-200 text-brand-700 font-medium'
                                        : 'border-slate-200 text-slate-700 hover:bg-slate-50'
                                        }`}
                                >
                                    Quantitative
                                </button>
                            </div>
                        </div>

                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
                            <Button
                                variant="primary"
                                className="w-full"
                                onClick={amplifyAchievements}
                                disabled={!hasNonEmptyAchievements || amplifying}
                            >
                                <Sparkles className="w-4 h-4 mr-2" />
                                {amplifying ? 'Amplifying...' : 'Amplify'}
                            </Button>
                        </div>
                    </div>

                    <div>
                        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200 h-full flex flex-col">
                            <div className="flex items-center justify-between mb-4">
                                <h3 className="text-lg font-medium text-slate-900">Results</h3>
                                {results.length > 0 && (
                                    <Button
                                        variant="secondary"
                                        size="sm"
                                        onClick={copyAll}
                                        className="flex items-center gap-2"
                                    >
                                        <CopyIcon className="w-4 h-4" />
                                        Copy All
                                    </Button>
                                )}
                            </div>

                            {results.length === 0 ? (
                                <div className="flex-1 flex items-center justify-center border-2 border-dashed border-slate-200 rounded-lg p-6">
                                    <p className="text-slate-400 text-center">
                                        Your amplified achievements will appear here
                                    </p>
                                </div>
                            ) : (
                                <div className="flex-1 overflow-auto space-y-4">
                                    {results.map((result, index) => (
                                        <div key={index} className="border border-slate-200 rounded-lg p-4 bg-slate-50">
                                            <div className="mb-3">
                                                <p className="text-xs font-semibold text-slate-500 uppercase mb-1">Original</p>
                                                <p className="text-sm text-slate-700">{result.original_achievement}</p>
                                            </div>
                                            <div>
                                                <p className="text-xs font-semibold text-slate-500 uppercase mb-1">Amplified</p>
                                                <p className="text-sm text-slate-900 font-medium">{result.rewritten_achievement}</p>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}

