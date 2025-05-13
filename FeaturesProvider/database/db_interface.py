from sqlalchemy import create_engine, Column, Integer, String, Text, Date, ForeignKey, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    country = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    github_url = Column(String(255), nullable=True)
    personal_website = Column(String(255), nullable=True)
    other_url = Column(String(255), nullable=True)
    about_me = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    # Relationships
    education = relationship("Education", back_populates="profile", cascade="all, delete-orphan")
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
    def __init__(self, db_url=None, test_mode=False):
        """Initialize database connection and session maker.

        Args:
            db_url (str, optional): Database connection URL. If None, uses default connection.
            test_mode (bool, optional): If True, use SQLite in-memory database for testing.
        """
        if test_mode:
            db_url = 'sqlite:///:memory:'
        elif db_url is None:
            db_host = os.getenv('DB_HOST', 'localhost')
            db_port = os.getenv('DB_PORT', '5432')
            db_user = os.getenv('DB_USER', 'features_user')
            db_pass = os.getenv('DB_PASSWORD', 'features_password')
            db_name = os.getenv('DB_NAME', 'features_db')

            db_url = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'

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

    def add_profile(self, session, profile_data):
        """Add a new profile to the database.

        Args:
            session: SQLAlchemy session.
            profile_data (dict): Dictionary containing profile information.

        Returns:
            Profile: The created profile object.
        """
        profile = Profile(**profile_data)
        session.add(profile)
        session.commit()
        return profile

    def get_profile(self, session, profile_id):
        """Get a profile by ID.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        return session.query(Profile).filter(Profile.id == profile_id).first()

    def get_profile_by_email(self, session, email):
        """Get a profile by email.

        Args:
            session: SQLAlchemy session.
            email (str): Email of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        return session.query(Profile).filter(Profile.email == email).first()

    def update_profile(self, session, profile_id, profile_data):
        """Update a profile.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to update.
            profile_data (dict): Dictionary containing updated profile information.

        Returns:
            Profile: The updated profile object if found, None otherwise.
        """
        profile = session.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None

        for key, value in profile_data.items():
            setattr(profile, key, value)

        session.commit()
        return profile

    def delete_profile(self, session, profile_id):
        """Delete a profile.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to delete.

        Returns:
            bool: True if deletion was successful, False otherwise.
        """
        profile = session.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return False

        session.delete(profile)
        session.commit()
        return True

    def add_education(self, session, profile_id, education_data):
        """Add education entry to a profile.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to add education to.
            education_data (dict): Dictionary containing education information.

        Returns:
            Education: The created education object, or None if profile not found.
        """
        profile = session.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None

        education_data['profile_id'] = profile_id
        education = Education(**education_data)
        session.add(education)
        session.commit()
        return education

    def delete_education(self, session, education_id):
        """Delete an education entry by ID.

        Args:
            session: SQLAlchemy session.
            education_id (int): ID of the education entry to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        education = session.query(Education).filter(Education.id == education_id).first()
        if not education:
            return False

        session.delete(education)
        session.commit()
        return True

    def add_experience(self, session, profile_id, experience_data):
        """Add experience entry to a profile.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to add experience to.
            experience_data (dict): Dictionary containing experience information.

        Returns:
            Experience: The created experience object, or None if profile not found.
        """
        profile = session.query(Profile).filter(Profile.id == profile_id).first()
        if not profile:
            return None

        experience_data['profile_id'] = profile_id
        experience = Experience(**experience_data)
        session.add(experience)
        session.commit()
        return experience

    def delete_experience(self, session, experience_id):
        """Delete an experience entry by ID.

        Args:
            session: SQLAlchemy session.
            experience_id (int): ID of the experience entry to delete.

        Returns:
            True if deleted successfully, False otherwise.
        """
        experience = session.query(Experience).filter(Experience.id == experience_id).first()
        if not experience:
            return False

        session.delete(experience)
        session.commit()
        return True

    def get_experiences(self, session, profile_id):
        """Get all experiences for a profile.

        Args:
            session: SQLAlchemy session.
            profile_id (int): ID of the profile to get experiences for.

        Returns:
            list: List of Experience objects.
        """
        return session.query(Experience).filter(Experience.profile_id == profile_id).all()

    # Additional convenience methods that don't require an explicit session
    # These methods create a session, perform the operation, and close the session

    def add_profile_auto(self, profile_data):
        """Add a new profile to the database (with automatic session handling).

        Args:
            profile_data (dict): Dictionary containing profile information.

        Returns:
            Profile: The created profile object.
        """
        session = self.get_session()
        try:
            return self.add_profile(session, profile_data)
        finally:
            self.close_session(session)

    def get_profile_auto(self, profile_id):
        """Get a profile by ID (with automatic session handling).

        Args:
            profile_id (int): ID of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        session = self.get_session()
        try:
            return self.get_profile(session, profile_id)
        finally:
            self.close_session(session)

    def get_profile_by_email_auto(self, email):
        """Get a profile by email (with automatic session handling).

        Args:
            email (str): Email of the profile to retrieve.

        Returns:
            Profile: The profile object if found, None otherwise.
        """
        session = self.get_session()
        try:
            return self.get_profile_by_email(session, email)
        finally:
            self.close_session(session)

    # Add this to the DatabaseManager class in db_interface.py
    def add_experience_auto(self, profile_id, experience_data):
        """Add experience entry to a profile (with automatic session handling).

        Args:
            profile_id (int): ID of the profile to add experience to.
            experience_data (dict): Dictionary containing experience information.

        Returns:
            Experience: The created experience object, or None if profile not found.
        """
        session = self.get_session()
        try:
            return self.add_experience(session, profile_id, experience_data)
        finally:
            self.close_session(session)

    def get_experiences_auto(self, profile_id):
        """Get all experiences for a profile (with automatic session handling).

        Args:
            profile_id (int): ID of the profile to get experiences for.

        Returns:
            list: List of Experience objects.
        """
        session = self.get_session()
        try:
            return self.get_experiences(session, profile_id)
        finally:
            self.close_session(session)
