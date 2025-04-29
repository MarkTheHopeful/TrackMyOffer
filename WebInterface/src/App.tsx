import React from 'react';
import { Navigation } from './components/navigation';
import { Button } from './components/ui/button';
import { BellIcon, FileTextIcon, Sparkles, SearchIcon, UserIcon, ServerIcon } from 'lucide-react';
import { LogIn } from './components/LogIn';
import { CVBuilder } from './components/cv-builder';
import { ApiDemo } from './components/ApiDemo';
import { CVReview } from './components/CVReview';
import { CoverLetter } from './components/CoverLetter';
import { ProfileForm } from './components/profile';
import { checkAuthStatus, authentify } from './api/backend';
import { LogOutButton } from "@/components/LogOutButton.tsx";
import { LandingPage } from './components/LandingPage';

function App() {
  const [activeView, setActiveView] = React.useState<'home' | 'cv-builder' | 'cv-review' | 'cover-letter' | 'api-demo' | 'log-in' | 'log-out' | 'profile'>('home');
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [isLoading, setIsLoading] = React.useState(true);

  React.useEffect(() => {
    console.log('Checking auth status...');
    checkAuthStatus().then((status) => {
      console.log('Auth status:', status.authenticated);
      setIsLoggedIn(status.authenticated);
      setIsLoading(false);
    }).catch((err) => {
      console.error('Auth check failed', err);
      setIsLoading(false);
    });
  }, []);

  // Add logging for activeView and isLoggedIn changes
  React.useEffect(() => {
    console.log('State updated:', { activeView, isLoggedIn });
  }, [activeView, isLoggedIn]);

  const handleLoginClick = () => {
    authentify();
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-brand-600"></div>
      </div>
    );
  }

  if (!isLoggedIn) {
    return <LandingPage onLoginClick={handleLoginClick} />;
  }

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
      case 'log-out':
        return <LogOutButton />;
      case 'profile':
        return <ProfileForm />;
      default:
        return (
          <div className="max-w-7xl mx-auto">
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
                activeView === 'api-demo' ? 'API Demo' :
                  activeView === 'profile' ? 'Profile' :
                    activeView === 'cv-review' ? 'CV Review' :
                      activeView === 'cover-letter' ? 'Cover Letter' :
                        'Welcome'}
          </h1>
          <div className="flex items-center space-x-4">
            <button className="p-2 hover:bg-brand-50 rounded-full text-slate-600 hover:text-brand-600 transition-colors">
              <BellIcon className="w-6 h-6" />
            </button>
            <Button variant="primary" className="flex items-center gap-2" onClick={() => setActiveView('log-out')}>
              <UserIcon className="w-4 h-4" />
              Log out
            </Button>
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