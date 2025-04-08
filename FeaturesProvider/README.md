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

### Run the API

To get started with the Features Provider, follow these simple steps:

1. First, install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

2. Set up your API key in your environment:

    ```bash
    export API_KEY="your-api-key"
    ```

3. Launch the API server:

    ```bash
    uvicorn main:app --reload
    ```

### Run Tests

Want to run the test suite? It's easy:

1. Install pytest if you haven't already:

    ```bash
    pip install pytest
    ```

2. Run the tests:

    ```bash
    pytest
    ```

That's it! You're all set. 🚀
