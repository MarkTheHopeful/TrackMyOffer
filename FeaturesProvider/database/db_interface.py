from sqlalchemy import create_engine, Column, Integer, String, Text, Date, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create base class for declarative models
Base = declarative_base()


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20))
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    summary = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    social_media = relationship("SocialMedia", back_populates="profile", uselist=False, cascade="all, delete-orphan")


class Education(Base):
    __tablename__ = "education"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    additional_info = Column(Text)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    profile = relationship("Profile", back_populates="education")


class SocialMedia(Base):
    __tablename__ = "social_media"

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id", ondelete="CASCADE"), nullable=False, unique=True)
    linkedin_url = Column(String(255))
    github_url = Column(String(255))
    personal_website = Column(String(255))
    other_links = Column(JSON)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    profile = relationship("Profile", back_populates="social_media")


class DatabaseManager:
    def __init__(self, test_mode=False):
        if test_mode:
            # Use SQLite in-memory database for testing
            self.engine = create_engine("sqlite:///:memory:")
        else:
            # Get database connection details from environment variables
            db_user = os.getenv("DB_USER", "features_user")
            db_password = os.getenv("DB_PASSWORD", "features_password")
            db_host = os.getenv("DB_HOST", "localhost")
            db_port = os.getenv("DB_PORT", "5432")
            db_name = os.getenv("DB_NAME", "features_db")

            # Create database URL
            database_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            self.engine = create_engine(database_url)

        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session"""
        return self.Session()

    def close_session(self, session):
        """Close a database session"""
        session.close()

    def add_profile(self, session, profile_data):
        """Add a new profile to the database"""
        profile = Profile(**profile_data)
        session.add(profile)
        session.commit()
        return profile

    def get_profile(self, session, profile_id):
        """Get a profile by ID"""
        return session.query(Profile).filter_by(id=profile_id).first()

    def get_profile_by_email(self, session, email):
        """Get a profile by email"""
        return session.query(Profile).filter_by(email=email).first()

    def update_profile(self, session, profile_id, update_data):
        """Update a profile"""
        profile = self.get_profile(session, profile_id)
        if profile:
            for key, value in update_data.items():
                setattr(profile, key, value)
            session.commit()
        return profile

    def delete_profile(self, session, profile_id):
        """Delete a profile and all related data"""
        profile = self.get_profile(session, profile_id)
        if profile:
            session.delete(profile)
            session.commit()
            return True
        return False

    def add_education(self, session, profile_id, education_data):
        """Add education record for a profile"""
        education_data["profile_id"] = profile_id
        education = Education(**education_data)
        session.add(education)
        session.commit()
        return education

    def add_social_media(self, session, profile_id, social_media_data):
        """Add social media information for a profile"""
        social_media_data["profile_id"] = profile_id
        social_media = SocialMedia(**social_media_data)
        session.add(social_media)
        session.commit()
        return social_media
