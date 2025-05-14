import { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { PlusIcon, Trash2Icon, SaveIcon } from 'lucide-react';
import { Experience } from '@/api/Experience';
import { getExperiences, createExperience, deleteExperience } from '@/api/backend';

interface ExperienceWithSelection extends Experience {
  selected: boolean;
  isNew?: boolean;
  isDeleted?: boolean;
  isModified?: boolean;
}

export function CVBuilder() {
  const [experiences, setExperiences] = useState<ExperienceWithSelection[]>([]);
  const [jobDescription, setJobDescription] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [hasChanges, setHasChanges] = useState(false);

  useEffect(() => {
    loadExperiences();
  }, []);

  const loadExperiences = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await getExperiences();
      setExperiences(data.map(exp => ({ ...exp, selected: true })));
      setHasChanges(false);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load experiences');
      console.error('Error loading experiences:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAddExperience = () => {
    const newExperience: ExperienceWithSelection = {
      id: 0,
      profile_id: 0,
      job_title: '',
      company: '',
      start_date: '',
      end_date: null,
      description: null,
      selected: true,
      isNew: true
    };
    setExperiences([...experiences, newExperience]);
    setHasChanges(true);
  };

  const updateExperience = (id: number, field: keyof ExperienceWithSelection, value: string | boolean | null) => {
    setExperiences(experiences.map(exp => {
      if (exp.id !== id) return exp;
      const updated = { ...exp, [field]: value };
      if (field !== 'selected' && !exp.isNew) {
        updated.isModified = true;
      }
      return updated;
    }));
    setHasChanges(true);
  };

  const removeExperience = (id: number) => {
    setExperiences(experiences.map(exp => {
      if (exp.id !== id) return exp;
      return { ...exp, isDeleted: true };
    }));
    setHasChanges(true);
  };

  const saveChanges = async () => {
    setIsLoading(true);
    setError(null);
    try {
      // First delete all deleted and modified experiences
      const toDelete = experiences.filter(exp => exp.isDeleted || exp.isModified);
      for (const exp of toDelete) {
        if (exp.id !== 0) { // Don't try to delete new experiences
          await deleteExperience(exp.id);
        }
      }

      // Then create all new and modified experiences
      const toCreate = experiences.filter(exp => exp.isNew || exp.isModified);
      for (const exp of toCreate) {
        const { selected, isNew, isDeleted, isModified, ...experienceData } = exp;
        await createExperience(experienceData);
      }

      // Reload experiences to get fresh data
      await loadExperiences();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save changes');
      console.error('Error saving changes:', err);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto">
      {error && (
        <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
          {error}
        </div>
      )}
      <div className="mb-8">
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold text-slate-900">Master CV</h2>
          <Button
            variant="primary"
            onClick={saveChanges}
            disabled={isLoading || !hasChanges}
            className="flex items-center gap-2"
          >
            <SaveIcon className="w-4 h-4" />
            Save Changes
          </Button>
        </div>
        <div className="space-y-6">
          {experiences.filter(exp => !exp.isDeleted).map(experience => (
            <div key={experience.id} className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <input
                    type="checkbox"
                    checked={experience.selected}
                    onChange={(e) => updateExperience(experience.id, 'selected', e.target.checked)}
                    className="w-4 h-4 text-brand-600 rounded border-slate-300 focus:ring-brand-500"
                  />
                  <h3 className="text-lg font-medium text-slate-900">Experience Entry</h3>
                </div>
                <button
                  onClick={() => removeExperience(experience.id)}
                  className="text-slate-400 hover:text-red-500 transition-colors"
                  disabled={isLoading}
                >
                  <Trash2Icon className="w-5 h-5" />
                </button>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Job Title</label>
                  <input
                    type="text"
                    value={experience.job_title}
                    onChange={(e) => updateExperience(experience.id, 'job_title', e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    placeholder="e.g., Senior Software Engineer"
                    disabled={isLoading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Company</label>
                  <input
                    type="text"
                    value={experience.company}
                    onChange={(e) => updateExperience(experience.id, 'company', e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    placeholder="e.g., Tech Corp"
                    disabled={isLoading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Start Date</label>
                  <input
                    type="date"
                    value={experience.start_date}
                    onChange={(e) => updateExperience(experience.id, 'start_date', e.target.value)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    disabled={isLoading}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">End Date</label>
                  <input
                    type="date"
                    value={experience.end_date || ''}
                    onChange={(e) => updateExperience(experience.id, 'end_date', e.target.value || null)}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    disabled={isLoading}
                  />
                </div>
                <div className="col-span-2">
                  <label className="block text-sm font-medium text-slate-700 mb-1">Description</label>
                  <textarea
                    value={experience.description || ''}
                    onChange={(e) => updateExperience(experience.id, 'description', e.target.value || null)}
                    rows={4}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500"
                    placeholder="Describe your responsibilities and achievements..."
                    disabled={isLoading}
                  />
                </div>
              </div>
            </div>
          ))}
          <Button onClick={handleAddExperience} className="w-full" disabled={isLoading}>
            <PlusIcon className="w-4 h-4 mr-2" />
            Add Experience
          </Button>
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-semibold text-slate-900 mb-4">Target Position</h2>
        <div className="bg-white rounded-xl p-6 shadow-lg shadow-slate-200/50 border border-slate-200">
          <label className="block text-sm font-medium text-slate-700 mb-1">
            Job Description or URL
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            rows={4}
            className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-brand-500 mb-4"
            placeholder="Paste job description or enter URL..."
            disabled={isLoading}
          />
          <Button variant="primary" className="w-full" disabled={isLoading}>
            Generate Tailored CV
          </Button>
        </div>
      </div>
    </div>
  );
}