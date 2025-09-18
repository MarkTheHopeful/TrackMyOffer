# Features Provider

This is the part that does the main work (features) of our application (or passes most of it to the external AI provider lmao). The responsibilities here are to provide an API for the back end for specific features.

Feature Provider consists of two main parts:

- Experience storage --- a database designed to store all valuable information about a user in a specific form (like their work experience, school projects, etc)
- Features subservices --- specific subparts responsible for one specific feature, be it extracting job information from provided page, generating a motivational letter for a user given the position or CV tailoring. They do not need to be separate services as in "separate applications", but there should be some logical separation between them.

It is supposed that at least part of the meaningful work is passed to an external AI provider/API, so some kind of accessor for such API is also required.

- Q: What exactly request dispatcher provides to the Features Provider?

  A: The API is not yet specified, but the idea is that it provides user id (so that their information can be retrieved from the experience storage) along with relevant to request data, be that job position description (or a link to it, in case of extractor), template for CV or something else.

- Q: Technology choice?

  A: Your choice, honestly. Still should be something understandable for others and something you already know (so we won't need to spend a sprint just learning new cool framework). Python + Flask?

- Q: How do we make requests to AI Provider? (Where to get AI key)?

  A: No idea yet, probably we can do it with some free-to-use API with low-profile LLM to begin with.

Btw, don't forget to update .gitignore

## How to run

### Docker

The easiest way to run the application is using Docker:

1. Build the Docker image:
   ```bash
   docker build -t features-provider .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 8000:8000 features-provider
   ```

You can customize the host, port, and API key using environment variables:
   ```bash
   docker run -p 9000:9000 -e PORT=9000 -e HOST=0.0.0.0 -e API_KEY=your-api-key features-provider
   ```

### Easy Setup

We've provided scripts to make setup and running easy:

1. Make sure you have Python 3.12 installed on your system.

2. The API key is already set up in the `.env` file for convenience. You can use the provided key or replace it with your own.

4. Run the application using the provided script:
   ```bash
   ./run.sh
   ```

The script will automatically:
- Create a virtual environment
- Install all required dependencies
- Start the server on port 8000

### Manual Setup

If you prefer to set up manually:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Ensure you have a `.env` file with the API key:
   ```
   API_KEY=your-api-key
   ```

5. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### API Endpoints

- `GET /`: Basic health check
- `POST /greet`: Accepts a JSON payload with a "name" field and returns an AI-generated greeting
- `POST /api/profile`: Create or update a user profile with personal information

    You can also specify a custom port:

    ```bash
    uvicorn main:app --reload --port 8000
    ```

### Run Tests

To run the test suite:

1. Ensure you have the virtual environment activated
2. Run:
   ```bash
   pytest
   ```

## Evaluation

The FeatureProvider test suite was executed in a clean virtual environment using Python 3.12.

- Command:
  ```bash
  python3.12 -m venv venv312 && source venv312/bin/activate && pip install -r requirements.txt && pytest -q
  ```

- Result:
  ```
  24 passed, 1 xfailed in 7.85s
  ```

- Notes:
  - The single xfail is an integration test that would contact the real AI model and is intentionally marked as expected-to-fail without network/API key.
  - Environment: macOS (Darwin 24.x), Python 3.12.7, isolated venv. No Docker/Postgres needed for tests.
  - Coverage highlights: Profile and Experience endpoints (create/list/error paths), cover-letter endpoint (mocked AI), cover-letter generator fallback, DB CRUD and relationships.
  - Representative checks: correct HTTP status codes (200/201/404/422/503), response schemas via Pydantic models, prompt content passed to AI mock.
  - See TESTING.md for details on structure, fixtures, mocking, and extending the suite.

### How to run database
Prerequisites: **Docker Desktop**
1. Make sure to download Docker from https://www.docker.com/get-started/.
2. Run:
    ```bash
   cd database
   ```
3. Run:
    ```bash
    docker compose up -d
   ```
   or 
    ```bash
    docker-compose up -d
   ```
4. The database will be accessible at:
    - Host: localhost
    - Port: 5432
    - Database: features_db
    - Username: features_user
    - Password: features_password
5. If you included pgAdmin, you can access it at [http://localhost:5050](http://localhost:5050)
    - Login with: admin@example.com
    - Password: admin_password
    - To connect to your database, create a new server connection with the connection details above (use "postgres" as the hostname instead of "localhost")

### How to check what is inside database

1. Run this command to open postgres console:

   ```bash
   docker exec -it profiles_db psql -U features_user -d features_db
   ```

2. Make SQL-query to get some data:

   ```sql
   SELECT * FROM profiles;
   ```

