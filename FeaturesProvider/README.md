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

### Easy Setup

We've provided scripts to make setup and running easy:

1. Make sure you have Python 3.8+ installed on your system.

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

### How to run database
1. go to the database dir
2. Run:
    ```bash
    docker-compose up -d
   ```
3. The database will be accessible at:
    - Host: localhost
    - Port: 5432
    - Database: features_db
    - Username: features_user
    - Password: features_password
4. If you included pgAdmin, you can access it at [http://localhost:5050](http://localhost:5050)
    - Login with: admin@example.com
    - Password: admin_password
    - To connect to your database, create a new server connection with the connection details above (use "postgres" as the hostname instead of "localhost")
