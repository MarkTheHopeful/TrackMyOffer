import React from 'react';
import { Navigation } from './components/navigation';
import { Button } from './components/ui/button';
import { BellIcon, FileTextIcon, PlusIcon, Sparkles, SearchIcon, UserIcon, ServerIcon } from 'lucide-react';
import { CVBuilder } from './components/cv-builder';
import { ApiDemo } from './components/ApiDemo';
import { CVReview } from './components/CVReview';
import { CoverLetter } from './components/CoverLetter';

function App() {
  const [activeView, setActiveView] = React.useState<'home' | 'cv-builder' | 'cv-review' | 'cover-letter' | 'api-demo'>('home');

  const renderContent = () => {
    switch (activeView) {
      case 'cv-builder':
        return <CVBuilder />;
      case 'cv-review':
        return <CVReview />;
      case 'cover-letter':
        return <CoverLetter />;
      case 'api-demo':
        return <ApiDemo />;
      default:
        return (
          <div className="max-w-7xl mx-auto">
            <div className="flex justify-end mb-8">
              <Button variant="secondary" className="flex items-center gap-2">
                <UserIcon className="w-4 h-4" />
                Log in / Register
              </Button>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              <div className="bg-white rounded-xl shadow-lg shadow-slate-200/50 border border-slate-200 p-6 hover:shadow-brand-100/50 hover:border-brand-200 transition-all">
                <div className="mb-4">
                  <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                    <Sparkles className="w-6 h-6 text-brand-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">Tailored CV Creation</h3>
                  <p className="text-slate-600 mt-2">Create your Master CV and auto-generate tailored versions for specific jobs</p>
                </div>
                <Button variant="primary" className="w-full" onClick={() => setActiveView('cv-builder')}>
                  Create CV
                </Button>
              </div>

              <div className="bg-white rounded-xl shadow-lg shadow-slate-200/50 border border-slate-200 p-6 hover:shadow-brand-100/50 hover:border-brand-200 transition-all">
                <div className="mb-4">
                  <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                    <SearchIcon className="w-6 h-6 text-brand-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">CV Review & Feedback</h3>
                  <p className="text-slate-600 mt-2">Get instant feedback and match scores for your CV against job descriptions</p>
                </div>
                <Button variant="primary" className="w-full" onClick={() => setActiveView('cv-review')}>
                  Review CV
                </Button>
              </div>

              <div className="bg-white rounded-xl shadow-lg shadow-slate-200/50 border border-slate-200 p-6 hover:shadow-brand-100/50 hover:border-brand-200 transition-all">
                <div className="mb-4">
                  <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                    <FileTextIcon className="w-6 h-6 text-brand-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">Cover Letter Generator</h3>
                  <p className="text-slate-600 mt-2">Generate personalized cover letters aligned with job descriptions</p>
                </div>
                <Button variant="primary" className="w-full" onClick={() => setActiveView('cover-letter')}>
                  Write Letter
                </Button>
              </div>

              <div className="bg-white rounded-xl shadow-lg shadow-slate-200/50 border border-slate-200 p-6 hover:shadow-brand-100/50 hover:border-brand-200 transition-all">
                <div className="mb-4">
                  <div className="w-12 h-12 bg-brand-100 rounded-lg flex items-center justify-center mb-4">
                    <ServerIcon className="w-6 h-6 text-brand-600" />
                  </div>
                  <h3 className="text-lg font-semibold text-slate-900">API Connectivity</h3>
                  <p className="text-slate-600 mt-2">Demo of backend connection and API functionality</p>
                </div>
                <Button variant="primary" className="w-full" onClick={() => setActiveView('api-demo')}>
                  View Demo
                </Button>
              </div>
            </div>
          </div>
        );
    }
  };

  return (
    <div className="flex h-screen bg-slate-50">
      <Navigation activeView={activeView} setActiveView={setActiveView} />

      <main className="flex-1 overflow-auto">
        <header className="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between sticky top-0 z-10">
          <h1 className="text-2xl font-semibold text-slate-900">
            {activeView === 'home' ? 'Welcome back!' :
              activeView === 'cv-builder' ? 'CV Builder' :
                activeView === 'cv-review' ? 'CV Review' :
                  activeView === 'cover-letter' ? 'Cover Letter' :
                    activeView === 'api-demo' ? 'API Demo' : 'Welcome'}
          </h1>
          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-brand-50 rounded-full text-slate-600 hover:text-brand-600 transition-colors">
              <BellIcon className="w-6 h-6" />
            </button>
            {activeView === 'home' && (
              <Button onClick={() => setActiveView('cv-builder')}>
                <PlusIcon className="w-4 h-4 mr-2" />
                New CV
              </Button>
            )}
          </div>
        </header>

        <div className="p-4 sm:p-6 md:p-8 max-w-full">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

export default App;