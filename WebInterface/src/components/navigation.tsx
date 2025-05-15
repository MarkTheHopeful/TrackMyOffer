import { BriefcaseIcon, FileTextIcon, HomeIcon, SettingsIcon, Sparkles, ServerIcon, PenIcon, UserIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface NavItemProps {
  icon: React.ReactNode;
  label: string;
  active?: boolean;
  onClick?: () => void;
}

const NavItem = ({ icon, label, active, onClick }: NavItemProps) => (
  <button
    onClick={onClick}
    className={cn(
      'flex items-center space-x-3 px-4 py-3 w-full rounded-lg transition-all',
      active
        ? 'bg-gradient-to-r from-brand-600 to-brand-500 text-white shadow-lg shadow-brand-500/25'
        : 'text-slate-600 hover:bg-brand-50 hover:text-brand-600'
    )}
  >
    {icon}
    <span className="font-medium">{label}</span>
  </button>
);

interface NavigationProps {
  activeView: string;
  setActiveView: (view: 'home' | 'cv-builder' | 'job-match-score' | 'cover-letter' | 'api-demo' | 'profile' | 'privacy-and-terms') => void;
}

export const Navigation = ({ activeView, setActiveView }: NavigationProps) => {
  return (
    <nav className="w-64 bg-white border-r border-slate-200 p-4">
      <div className="flex items-center gap-3 px-4 py-3 mb-6">
        <Sparkles className="w-8 h-8 text-brand-500" />
        <span className="text-xl font-semibold bg-gradient-to-r from-brand-600 to-accent-600 bg-clip-text text-transparent">
          TrackMyOffer
        </span>
      </div>
      <div className="space-y-2">
        <NavItem
          icon={<HomeIcon size={20} />}
          label="Dashboard"
          active={activeView === 'home'}
          onClick={() => setActiveView('home')}
        />
        <NavItem
          icon={<UserIcon size={20} />}
          label="Profile"
          active={activeView === 'profile'}
          onClick={() => setActiveView('profile')}
        />
        <NavItem
          icon={<FileTextIcon size={20} />}
          label="CV Builder"
          active={activeView === 'cv-builder'}
          onClick={() => setActiveView('cv-builder')}
        />
        <NavItem
          icon={<BriefcaseIcon size={20} />}
          label="Job Match Score"
          active={activeView === 'job-match-score'}
          onClick={() => setActiveView('job-match-score')}
        />
        <NavItem
          icon={<PenIcon size={20} />}
          label="Cover Letter"
          active={activeView === 'cover-letter'}
          onClick={() => setActiveView('cover-letter')}
        />
        <NavItem
          icon={<ServerIcon size={20} />}
          label="API Demo"
          active={activeView === 'api-demo'}
          onClick={() => setActiveView('api-demo')}
        />
        <NavItem
          icon={<SettingsIcon size={20} />}
          label="Settings"
          active={activeView === 'settings'}
        />
        <NavItem
            icon={<FileTextIcon size={20} />}
            label="Privacy and Terms"
            active={activeView === 'privacy-and-terms'}
            onClick={() => setActiveView('privacy-and-terms')}
        />
      </div>
    </nav>
  );
};