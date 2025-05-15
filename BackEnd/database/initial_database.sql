-- Create the user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    email VARCHAR (255) PRIMARY KEY,
    profile_id INTEGER NOT NULL
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_profile_id ON user_profiles(profile_id);