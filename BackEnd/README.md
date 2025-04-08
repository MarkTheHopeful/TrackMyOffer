## Back End

The "Proxy" part, responsible for the communication between web interface and the features provider, abstracting auth, user information and requests handling from the features provider.

Back end consists of two main parts:
* Request dispatcher (the part responsible for, well, transforming and passing requests from a user to the features provider, as well as serving as a result reception point for responses from the features provider. 
* Utility database, to store needed user information which is not directly related to the work experience, such as tokens, correspondence between auth tokens and user ids, probably some preferences etc.

Q: What is the specific architecture for the back end?
A: The inner workings are not defined yet, this is one of the tasks. However, it might be useful to design an API for interaction with both Web Interface and Features Provider.

Q: What is the technology choice? 
A: Idk, honestly. Probably we will come up with something for the API documentation soon, but as for the service itself -- that's up to the team responsible for this part. Python + Flask?

Btw, don't forget to update .gitignore so we won't have to deal with .idea on master.

## Current Implementation

The backend is currently implemented using Kotlin and Ktor. It provides a simple API with the following endpoints:
- `GET /v0/`: Returns a "Hello World!" message
- `GET /v0/hello`: Returns a greeting with the request origin
- `GET /features/v0/hello`: Will call the feature provider service (currently a TODO)

Run with
```
./gradlew run
```

It is possible to specify deployment port and host, as well as host and port of the feature provider 
(below are defaults) via env:
```
PORT=8080 HOST=0.0.0.0 PROVIDER_PORT=8081 PROVIDER_HOST=0.0.0.0 ./gradlew run 
```

After running, try requesting something e.g. via curl:
```
curl 0.0.0.0:8080/v0/hello
```

## API Documentation

The API is documented using the OpenAPI 3.0 specification. The specification file is located at:
```
src/main/resources/openapi.yaml
```

This specification serves as a base for future development and can be extended as new endpoints are added.

### Swagger UI

The API documentation is available through Swagger UI, which provides an interactive interface to explore and test the API. You can access it at:
```
http://localhost:8080/v0/swagger
```

The Swagger UI is served by the Ktor Swagger plugin and uses the specification file mentioned above.
