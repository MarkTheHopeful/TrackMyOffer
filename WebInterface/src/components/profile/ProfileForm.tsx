import React, { useState, useEffect } from 'react';
import { Button } from '../ui/button';
import { UserIcon, GraduationCapIcon, LinkedinIcon, GithubIcon, ExternalLinkIcon, SaveIcon, PlusIcon, TrashIcon, PencilIcon } from 'lucide-react';
import { fetchProfileInfo, updateProfileInfo, createEducationEntry, deleteEducationEntry, saveProfileData } from '@/api/backend.ts';
import { ProfileData } from '@/api/ProfileData.ts';
import { EducationEntry } from '@/api/EducationEntry.ts';

export function ProfileForm() {
  const [activeTab, setActiveTab] = useState<'personal' | 'education' | 'social' | 'summary'>('personal');
  const [profileData, setProfileData] = useState<ProfileData>({
    education: []
  });
  const [currentEducation, setCurrentEducation] = useState<EducationEntry>({
    id: '',
    institution: '',
    degree: '',
    startDate: '',
    endDate: '',
    additionalInfo: ''
  });
  const [editMode, setEditMode] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    console.log('ProfileForm mounted, fetching profile data...');
    fetchProfileInfo()
      .then(
        data => {
          console.log('Received profile data:', data);
          setProfileData(data);
        }
      )
      .catch(
        err => {
          console.log('Error fetching profile data:', err)
        }
      );
  }, []);

  const handleProfileChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setProfileData((prev: ProfileData) => ({ ...prev, [name]: value }));
  };

  const saveProfile = async () => {
    setIsLoading(true);
    setError(null);
    try {
      if (activeTab === 'personal') {
        const { education, ...profileDataWithoutEducation } = profileData;
        await saveProfileData(profileDataWithoutEducation);
      } else {
        await updateProfileInfo(profileData);
      }
      alert('Profile updated successfully');
    } catch (err) {
      if (err instanceof Error) {
        if (err.message === 'Request timed out') {
          alert('Profile update request timed out. Please try again later.');
        } else {
          console.error('Failed to update profile:', err);
          alert('Failed to update profile. See console for details.');
        }
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleEducationChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setCurrentEducation((prev: EducationEntry) => ({ ...prev, [name]: value }));
  };

  const addEducationEntry = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const { id, ...educationData } = currentEducation;
      const newEntry = await createEducationEntry(educationData);
      setProfileData((prev: ProfileData) => ({
        ...prev,
        education: [...(prev.education || []), newEntry]
      }));
      setCurrentEducation({
        id: '',
        institution: '',
        degree: '',
        startDate: '',
        endDate: '',
        additionalInfo: ''
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
        alert('Failed to add education entry: ' + err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const editEducationEntry = (id: string) => {
    const entryToEdit = profileData.education?.find((entry: EducationEntry) => entry.id === id);
    if (entryToEdit) {
      setCurrentEducation(entryToEdit);
      setEditMode(id);
    }
  };

  const updateEducationEntry = async () => {
    if (!editMode) return;

    setIsLoading(true);
    setError(null);
    try {
      await deleteEducationEntry(editMode);
      const { id, ...educationData } = currentEducation;
      const newEntry = await createEducationEntry(educationData);

      setProfileData((prev: ProfileData) => ({
        ...prev,
        education: prev.education?.map((entry: EducationEntry) =>
          entry.id === editMode ? newEntry : entry
        ) || []
      }));

      setCurrentEducation({
        id: '',
        institution: '',
        degree: '',
        startDate: '',
        endDate: '',
        additionalInfo: ''
      });
      setEditMode(null);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
        alert('Failed to update education entry: ' + err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleDeleteEducation = async (id: string) => {
    if (!confirm('Are you sure you want to delete this education entry?')) return;

    setIsLoading(true);
    setError(null);
    try {
      await deleteEducationEntry(id);
      setProfileData((prev: ProfileData) => ({
        ...prev,
        education: prev.education?.filter((entry: EducationEntry) => entry.id !== id) || []
      }));

      if (editMode === id) {
        setEditMode(null);
        setCurrentEducation({
          id: '',
          institution: '',
          degree: '',
          startDate: '',
          endDate: '',
          additionalInfo: ''
        });
      }
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
        alert('Failed to delete education entry: ' + err.message);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg border border-slate-200 p-6">
      <h2 className="text-2xl font-semibold text-slate-900 mb-6">Profile Information</h2>

      <div className="flex border-b border-slate-200 mb-6">
        <button
          onClick={() => setActiveTab('personal')}
          className={`px-4 py-2 font-medium text-sm ${activeTab === 'personal'
            ? 'text-brand-600 border-b-2 border-brand-600'
            : 'text-slate-600 hover:text-brand-600'
            }`}
        >
          <div className="flex items-center gap-2">
            <UserIcon className="w-4 h-4" />
            Personal Information
          </div>
        </button>
        <button
          onClick={() => setActiveTab('education')}
          className={`px-4 py-2 font-medium text-sm ${activeTab === 'education'
            ? 'text-brand-600 border-b-2 border-brand-600'
            : 'text-slate-600 hover:text-brand-600'
            }`}
        >
          <div className="flex items-center gap-2">
            <GraduationCapIcon className="w-4 h-4" />
            Education
          </div>
        </button>
        <button
          onClick={() => setActiveTab('social')}
          className={`px-4 py-2 font-medium text-sm ${activeTab === 'social'
            ? 'text-brand-600 border-b-2 border-brand-600'
            : 'text-slate-600 hover:text-brand-600'
            }`}
        >
          <div className="flex items-center gap-2">
            <LinkedinIcon className="w-4 h-4" />
            Social Media
          </div>
        </button>
        <button
          onClick={() => setActiveTab('summary')}
          className={`px-4 py-2 font-medium text-sm ${activeTab === 'summary'
            ? 'text-brand-600 border-b-2 border-brand-600'
            : 'text-slate-600 hover:text-brand-600'
            }`}
        >
          <div className="flex items-center gap-2">
            <ExternalLinkIcon className="w-4 h-4" />
            Summary
          </div>
        </button>
      </div>

      {activeTab === 'personal' && (
        <div className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">First Name</label>
              <input
                type="text"
                name="first_name"
                value={profileData.first_name}
                onChange={handleProfileChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Last Name</label>
              <input
                type="text"
                name="last_name"
                value={profileData.last_name}
                onChange={handleProfileChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Email Address</label>
            <input
              type="email"
              name="email"
              value={profileData.email}
              onChange={handleProfileChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Phone Number (Optional)</label>
            <input
              type="tel"
              name="phone"
              value={profileData.phone}
              onChange={handleProfileChange}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">City</label>
              <input
                type="text"
                name="city"
                value={profileData.city}
                onChange={handleProfileChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">State/Province</label>
              <input
                type="text"
                name="state"
                value={profileData.state}
                onChange={handleProfileChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-slate-700 mb-1">Country</label>
              <input
                type="text"
                name="country"
                value={profileData.country}
                onChange={handleProfileChange}
                className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'education' && (
        <div className="space-y-6">
          {profileData.education && profileData.education.length > 0 && (
            <div className="space-y-4">
              {profileData.education.map((entry) => (
                <div
                  key={entry.id}
                  className="bg-white p-4 rounded-lg border border-slate-200 hover:border-brand-300 transition-all"
                >
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="text-lg font-medium text-slate-900">
                      {entry.institution || 'Untitled Institution'}
                    </h3>
                    <div className="flex space-x-2">
                      <button
                        onClick={() => editEducationEntry(entry.id)}
                        className="p-1 text-slate-400 hover:text-brand-600 rounded-full hover:bg-brand-50"
                        disabled={isLoading}
                      >
                        <PencilIcon className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => handleDeleteEducation(entry.id)}
                        className="p-1 text-slate-400 hover:text-red-600 rounded-full hover:bg-red-50"
                        disabled={isLoading}
                      >
                        <TrashIcon className="w-4 h-4" />
                      </button>
                    </div>
                  </div>

                  {entry.degree && (
                    <p className="text-sm text-slate-700 mb-1">{entry.degree}</p>
                  )}

                  {(entry.startDate || entry.endDate) && (
                    <p className="text-sm text-slate-500 mb-1">
                      {entry.startDate && new Date(entry.startDate).getFullYear()}
                      {entry.startDate && entry.endDate && ' - '}
                      {entry.endDate && new Date(entry.endDate).getFullYear()}
                    </p>
                  )}

                  {entry.additionalInfo && (
                    <p className="text-sm text-slate-600 mt-2">{entry.additionalInfo}</p>
                  )}
                </div>
              ))}
            </div>
          )}

          <div className="bg-slate-50 p-4 rounded-lg border border-slate-200">
            <h3 className="text-lg font-medium text-slate-900 mb-4">
              {editMode ? 'Edit Education Entry' : 'Add Education Entry'}
            </h3>

            <div className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Educational Institution</label>
                <input
                  type="text"
                  name="institution"
                  value={currentEducation.institution}
                  onChange={handleEducationChange}
                  placeholder="University, College or School name"
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Academic Degree and Specialty</label>
                <input
                  type="text"
                  name="degree"
                  value={currentEducation.degree}
                  onChange={handleEducationChange}
                  placeholder="e.g. Bachelor's degree in Computer Science"
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                />
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">Start Date</label>
                  <input
                    type="date"
                    name="startDate"
                    value={currentEducation.startDate}
                    onChange={handleEducationChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-700 mb-1">End Date</label>
                  <input
                    type="date"
                    name="endDate"
                    value={currentEducation.endDate}
                    onChange={handleEducationChange}
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-700 mb-1">Additional Information</label>
                <textarea
                  name="additionalInfo"
                  value={currentEducation.additionalInfo}
                  onChange={handleEducationChange}
                  placeholder="Relevant term papers, honors theses, graduation papers, or projects"
                  rows={3}
                  className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
                ></textarea>
              </div>
            </div>

            <div className="flex justify-end mt-4">
              {editMode ? (
                <div className="flex space-x-3">
                  <Button
                    variant="ghost"
                    onClick={() => {
                      setEditMode(null);
                      setCurrentEducation({
                        id: '',
                        institution: '',
                        degree: '',
                        startDate: '',
                        endDate: '',
                        additionalInfo: ''
                      });
                    }}
                    disabled={isLoading}
                  >
                    Cancel
                  </Button>
                  <Button
                    variant="primary"
                    onClick={() => handleDeleteEducation(editMode)}
                    disabled={isLoading}
                    className="bg-red-600 hover:bg-red-700"
                  >
                    Delete
                  </Button>
                  <Button
                    variant="primary"
                    onClick={updateEducationEntry}
                    disabled={isLoading}
                  >
                    Save Changes
                  </Button>
                </div>
              ) : (
                <Button
                  variant="primary"
                  className="flex items-center gap-2"
                  onClick={addEducationEntry}
                  disabled={isLoading}
                >
                  <PlusIcon className="w-4 h-4" />
                  Add Education Entry
                </Button>
              )}
            </div>
          </div>
        </div>
      )}

      {activeTab === 'social' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">LinkedIn URL</label>
            <div className="flex">
              <div className="bg-slate-100 flex items-center px-3 border-y border-l border-slate-300 rounded-l-lg">
                <LinkedinIcon className="w-5 h-5 text-slate-500" />
              </div>
              <input
                type="url"
                name="linkedin_url"
                value={profileData.linkedin_url}
                onChange={handleProfileChange}
                placeholder="https://linkedin.com/in/yourprofile"
                className="w-full px-3 py-2 border border-slate-300 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">GitHub URL</label>
            <div className="flex">
              <div className="bg-slate-100 flex items-center px-3 border-y border-l border-slate-300 rounded-l-lg">
                <GithubIcon className="w-5 h-5 text-slate-500" />
              </div>
              <input
                type="url"
                name="github_url"
                value={profileData.github_url}
                onChange={handleProfileChange}
                placeholder="https://github.com/yourusername"
                className="w-full px-3 py-2 border border-slate-300 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Personal Website</label>
            <div className="flex">
              <div className="bg-slate-100 flex items-center px-3 border-y border-l border-slate-300 rounded-l-lg">
                <ExternalLinkIcon className="w-5 h-5 text-slate-500" />
              </div>
              <input
                type="url"
                name="personal_website"
                value={profileData.personal_website}
                onChange={handleProfileChange}
                placeholder="https://yourwebsite.com"
                className="w-full px-3 py-2 border border-slate-300 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">Other Relevant Links</label>
            <div className="flex">
              <div className="bg-slate-100 flex items-center px-3 border-y border-l border-slate-300 rounded-l-lg">
                <ExternalLinkIcon className="w-5 h-5 text-slate-500" />
              </div>
              <input
                type="url"
                name="other_url"
                value={profileData.other_url}
                onChange={handleProfileChange}
                placeholder="https://behance.net/portfolio or https://twitter.com/username"
                className="w-full px-3 py-2 border border-slate-300 rounded-r-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      )}

      {activeTab === 'summary' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-medium text-slate-700 mb-1">About Me</label>
            <textarea
              name="about_me"
              value={profileData.about_me}
              onChange={handleProfileChange}
              placeholder="Tell us about yourself, your key skills, achievements, and career aspirations..."
              rows={8}
              className="w-full px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-500 focus:border-transparent"
            ></textarea>
            <p className="text-sm text-slate-500 mt-2">
              This summary will help introduce you and highlight your personal brand, unique skills, and career motivation.
            </p>
          </div>
        </div>
      )}

      <div className="flex justify-end mt-8">
        <Button
          variant="primary"
          className="flex items-center gap-2"
          onClick={saveProfile}
          disabled={isLoading}
        >
          <SaveIcon className="w-4 h-4" />
          Save Profile
        </Button>
      </div>
    </div>
  );
} 
