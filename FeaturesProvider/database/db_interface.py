from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, DateTime, func, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    phone = Column(String(20), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(100), nullable=False)
    country = Column(String(100), nullable=False)
    summary = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
    social_media = relationship("SocialMedia", back_populates="profile", uselist=False, cascade="all, delete-orphan")
    experience = relationship("Experience", back_populates="profile", cascade="all, delete-orphan")


class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    institution = Column(String(255), nullable=False)
    degree = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    additional_info = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationship
    profile = relationship("Profile", back_populates="education")


class SocialMedia(Base):
    __tablename__ = 'social_media'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False, unique=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    personal_website = Column(String(255), nullable=True)
    other_links = Column(JSON, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationship
    profile = relationship("Profile", back_populates="social_media")


class Experience(Base):
    __tablename__ = 'experience'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profiles.id', ondelete='CASCADE'), nullable=False)
    job_title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationship
    profile = relationship("Profile", back_populates="experience")


class DatabaseManager:
    def __init__(self, db_url=None):
        """Initialize database connection and session maker.

        Args:
            db_url (str, optional): Database connection URL. If None, uses default SQLite connection.
        """
        if db_url is None:
            db_url = 'postgresql://features_user:features_password@localhost:5432/features_db'

        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Create all tables in the database if they don't exist."""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Get a new database session.

        Returns:
            Session: A new SQLAlchemy session.
        """
        return self.Session()

    def close_session(self, session):
        """Close a database session.

        Args:
            session: SQLAlchemy session to close.
        """
        if session:
            session.close()

    def add_profile(self, profile_data):
        """Add a new profile to the database.

        Args:
            profile_data (dict): Dictionary containing profile information.

        Returns:
            Profile: The created profile object.
        """
        session = self.get_session()
        try:
            profile = Profile(**profile_data)
            session.add(profile)
            session.commit()
            return profile
        finally:
            self.close_session(session)

    def get_profile(self, profile_id):
        """Get a profile by ID.

        Args:
            profile_id (int): ID of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        session = self.get_session()
        try:
            return session.query(Profile).filter(Profile.id == profile_id).first()
        finally:
            self.close_session(session)

    def get_profile_by_email(self, email):
        """Get a profile by email.

        Args:
            email (str): Email of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        session = self.get_session()
        try:
            return session.query(Profile).filter(Profile.email == email).first()
        finally:
            self.close_session(session)

    def update_profile(self, profile_id, profile_data):
        """Update a profile.

        Args:
            profile_id (int): ID of the profile to update.
            profile_data (dict): Dictionary containing updated profile information.

        Returns:
            bool: True if update was successful, False otherwise.
        """
        session = self.get_session()
        try:
            profile = session.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return False

            for key, value in profile_data.items():
                setattr(profile, key, value)

            session.commit()
            return True
        finally:
            self.close_session(session)

    def delete_profile(self, profile_id):
        """Delete a profile.

        Args:
            profile_id (int): ID of the profile to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        session = self.get_session()
        try:
            profile = session.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return False

            session.delete(profile)
            session.commit()
            return True
        finally:
            self.close_session(session)

    def add_education(self, profile_id, education_data):
        """Add education entry to a profile.

        Args:
            profile_id (int): ID of the profile to add education to.
            education_data (dict): Dictionary containing education information.

        Returns:
            Education: The created education object, or None if profile not found.
        """
        session = self.get_session()
        try:
            profile = session.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return None

            education_data['profile_id'] = profile_id
            education = Education(**education_data)
            session.add(education)
            session.commit()
            return education
        finally:
            self.close_session(session)

    def add_social_media(self, profile_id, social_media_data):
        """Add or update social media for a profile.

        Args:
            profile_id (int): ID of the profile to add social media to.
            social_media_data (dict): Dictionary containing social media information.

        Returns:
            SocialMedia: The created or updated social media object, or None if profile not found.
        """
        session = self.get_session()
        try:
            profile = session.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return None

            social_media = session.query(SocialMedia).filter(SocialMedia.profile_id == profile_id).first()

            if social_media:
                # Update existing
                for key, value in social_media_data.items():
                    setattr(social_media, key, value)
            else:
                # Create new
                social_media_data['profile_id'] = profile_id
                social_media = SocialMedia(**social_media_data)
                session.add(social_media)

            session.commit()
            return social_media
        finally:
            self.close_session(session)

    def add_experience(self, profile_id, experience_data):
        """Add experience entry to a profile.

        Args:
            profile_id (int): ID of the profile to add experience to.
            experience_data (dict): Dictionary containing experience information.

        Returns:
            Experience: The created experience object, or None if profile not found.
        """
        session = self.get_session()
        try:
            profile = session.query(Profile).filter(Profile.id == profile_id).first()
            if not profile:
                return None

            experience_data['profile_id'] = profile_id
            experience = Experience(**experience_data)
            session.add(experience)
            session.commit()
            return experience
        finally:
            self.close_session(session)

    def get_experiences(self, profile_id):
        """Get all experiences for a profile.

        Args:
            profile_id (int): ID of the profile to get experiences for.

        Returns:
            list: List of Experience objects.
        """
        session = self.get_session()
        try:
            return session.query(Experience).filter(Experience.profile_id == profile_id).all()
        finally:
            self.close_session(session)
