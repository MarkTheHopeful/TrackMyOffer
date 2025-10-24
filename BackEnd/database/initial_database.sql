-- Create the user_profiles table
CREATE TABLE IF NOT EXISTS user_profiles (
    email VARCHAR (255) PRIMARY KEY,
    profile_id INTEGER NOT NULL
);

-- Create indexes for faster lookups
CREATE INDEX IF NOT EXISTS idx_user_profiles_email ON user_profiles(email);
CREATE INDEX IF NOT EXISTS idx_user_profiles_profile_id ON user_profiles(profile_id);

-- Track per-day user activity
CREATE TABLE IF NOT EXISTS user_activity_logs (
    email VARCHAR(255) NOT NULL,
    activity_date DATE NOT NULL,
    PRIMARY KEY (email, activity_date)
);

-- Maintain current streak metadata
CREATE TABLE IF NOT EXISTS user_streaks (
    email VARCHAR(255) PRIMARY KEY,
    current_streak INTEGER NOT NULL,
    last_active_date DATE NOT NULL
);
