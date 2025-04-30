import { Button } from './ui/button';
import { Sparkles, FileText, Search, Shield } from 'lucide-react';

export function LandingPage({ onLoginClick }: { onLoginClick: () => void }) {
    return (
        <div className="min-h-screen bg-gradient-to-b from-slate-50 to-white">
            {/* Hero Section */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
                <div className="text-center">
                    <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-5xl md:text-6xl">
                        <span className="block">Elevate Your Job Applications</span>
                        <span className="block text-brand-600">With AI-Powered Documents</span>
                    </h1>
                    <p className="mt-3 max-w-md mx-auto text-base text-gray-500 sm:text-lg md:mt-5 md:text-xl md:max-w-3xl">
                        Create tailored CVs, generate personalized cover letters, and get AI-powered insights to make your job applications stand out.
                    </p>
                    <div className="mt-5 max-w-md mx-auto sm:flex sm:justify-center md:mt-8">
                        <Button
                            variant="primary"
                            className="rounded-md px-8 py-3 text-base font-medium shadow-sm hover:bg-brand-700 md:py-4 md:text-lg md:px-10"
                            onClick={onLoginClick}
                        >
                            Get Started
                        </Button>
                    </div>
                </div>
            </div>

            {/* Features Section */}
            <div className="py-16 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="grid grid-cols-1 gap-8 md:grid-cols-2 lg:grid-cols-3">
                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                                <Sparkles className="w-6 h-6 text-brand-600" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900">Smart CV Builder</h3>
                            <p className="mt-2 text-gray-500">
                                Create professional CVs tailored to specific job positions with AI assistance.
                            </p>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                                <FileText className="w-6 h-6 text-brand-600" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900">Cover Letter Generation</h3>
                            <p className="mt-2 text-gray-500">
                                Generate personalized cover letters automatically tailored to specific job positions.
                            </p>
                        </div>

                        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
                            <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                                <Search className="w-6 h-6 text-brand-600" />
                            </div>
                            <h3 className="text-lg font-semibold text-gray-900">CV Analysis</h3>
                            <p className="mt-2 text-gray-500">
                                Get instant feedback on your CV and match scores against job descriptions.
                            </p>
                        </div>
                    </div>
                </div>
            </div>

            {/* Trust Section */}
            <div className="bg-gray-50 py-16">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-center gap-2 text-gray-500 mb-8">
                        <Shield className="w-5 h-5" />
                        <span>Secure Login with Google</span>
                    </div>
                </div>
            </div>
        </div>
    );
} 