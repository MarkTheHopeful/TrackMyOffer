-- Profiles table for personal information
CREATE TABLE profiles (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    country VARCHAR(100),
    state VARCHAR(100),
    city VARCHAR(100),
    phone VARCHAR(20),  -- Optional field
    linkedin_url VARCHAR(255),
    github_url VARCHAR(255),
    personal_website VARCHAR(255),
    other_url VARCHAR(255),
    about_me TEXT,  -- For "about me" information
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Add index on email for faster lookups
CREATE INDEX idx_profiles_email ON profiles(email);

-- Education table (can have multiple entries per profile)
CREATE TABLE education (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER NOT NULL,
    institution VARCHAR(255) NOT NULL,  -- Education institution
    degree VARCHAR(255) NOT NULL,       -- Academic degree and specialty
    start_date DATE NOT NULL,
    end_date DATE,                      -- Can be null if ongoing
    additional_info TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Add index on profile_id for faster joins
CREATE INDEX idx_education_profile_id ON education(profile_id);

-- Experience table (can have multiple entries per profile)
CREATE TABLE experience (
    id SERIAL PRIMARY KEY,
    profile_id INTEGER NOT NULL,
    job_title VARCHAR(255) NOT NULL,
    company VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE,  -- Can be null if current job
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Add index on profile_id for faster joins
CREATE INDEX idx_experience_profile_id ON experience(profile_id);

-- Create trigger function to update the "updated_at" timestamp automatically
CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for each table
CREATE TRIGGER update_profiles_timestamp
BEFORE UPDATE ON profiles
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_education_timestamp
BEFORE UPDATE ON education
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();

CREATE TRIGGER update_experience_timestamp
BEFORE UPDATE ON experience
FOR EACH ROW
EXECUTE FUNCTION update_modified_column();