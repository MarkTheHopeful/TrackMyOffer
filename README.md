# TrackMyOffer

## What is TrackMyOffer?

TrackMyOffer is a job application helper platform. It is a web platform that offers intelligent, tailored CV and cover letter creation. 

It stores your comprehensive career history and project experience in a “Master CV” and dynamically selects the most relevant sections to match job requirements when applying for a specific position. 

It also allows to check whether there is a "match" between a position provided and you, given all experience and information you provided.


## Project stucture

To the user, only from part, that is, Web Interface, is accessible, while everything else is abstracted and unseen to the user. Inside, the project is separated into three main modules:
- Web Interface, serving as a front end and written in TypeScript using React
- Back End, serving as a request dispatcher and handler of all utility functions, not related to work with CV itself, written in Kotlin using Ktor library
- Features Provider, serving as the main logic handler behind all the CV work and AI interaction, separated into many specific functions for i.e. extraction of job position information given text or link, storage of users' experience and so forth

Apart from what is implemented by us, several features are externalized, such as auth provider (implemented using Google OAuth) and AI models themselves, being served through OpenAI API.

Communication between the three modules is done using HTTP protocol specified in openapi files.

For more in-depth description of parts' architecture, use the following links: [Web Interface README](WebInterface/README.md), [Back End README](BackEnd/README.md) and [Feature Provider README](FeaturesProvider/README.md).

### Requirements & Architecture 

- The Requirements Book for the project is available via this [link](https://docs.google.com/document/d/1xXU2xOTpktsWVINS9sxt_Pv6vnwDQvh9NQTqpTrnQbo/edit?usp=sharing). 
- The high-level architecture diagram is available via this [link](https://drive.google.com/file/d/1jBHv_NsWErqjyx7iRrGBuINruEsCgRWE/view?usp=sharing).
  - A document with reasoning behind the chosen architecture design is available via this [link](https://docs.google.com/document/d/1OYZI9EdXdObnDyrL7oCGbjBhDP-Oa-lCwMkZBPdz6ZA/edit?usp=sharing).


## How to run it

### Docker

To correctly run all the subsystems, update .env files:
- [FeaturesProvider/.env](FeaturesProvider/.env): put your API_KEY (otherwise AI features won't work) like this
```
API_KEY=...
```
- [BackEnd/.env](BackEnd/.env): put CLIENT_ID and CLIENT_SECRET (otherwise Google OAuth won't work) like this:
```
CLIENT_ID=...
CLIENT_SECRET=...
```

**MAKE SURE TO NOT COMMIT THE SECRETS AND KEYS**: the `.env` files are tracked! 

Run
```
docker compose up -d
```

It should run web, back, features provider and database for FP. 

Alternatively (and I highly suggest that),
go to [docker-compose.yaml](docker-compose.yaml) and hit the green run button near the `services` in IDEA.

#### Troubleshooting 

If you happen to see something like this:
```
 > [web build 6/7] COPY . .:
------
failed to solve: cannot copy to non-directory: /var/lib/docker/overlay2/k899yl6b2obij7zmsde2rezdg/merged/app/node_modules/@eslint/js
```

Go to `WebInterface` subdirectory and ensure there is no `node_modules` present (delete them if they are). 

### Script

To run all three services together, try out [run_local.sh](run_local.sh) script. Ensure to:
- put your model API key at the top of the script
- install all the requirements for all three parts separately

Logs from services will be available in `logs` directory

## How to test it

Tests are usually ran as part of CI workflows (described further in this README), both component and integration. However, if you want to test it locally, you can look at how tests are implemented in specific parts, as described in [Web Interface README](WebInterface/README.md), [Back End README](BackEnd/README.md) and [Feature Provider README](FeaturesProvider/README.md).

## Continuous Integration

The CI of the project is provided by GitHub Actions and aims to perform automated verification of the project after each change.
It includes module-specific compilation checks and unit tests as well as a run of integration tests to ensure connectivity of all the components. 
The workflow files are located under the [.github/workflows](.github/workflows) directory under descriptive names.

Component-specific workflows are executed for each commit
changing either the corresponding workflow file or any tracked file in the component's directory.

Integration tests are slower and heavier; thus they are executed only on pull requests targeting the main branch.

Merge of a pull request to the target branch is possible only when all the relevant checks are passing.

Below are the descriptions and requirements of each workflow.

### [backend.yaml](.github/workflows/backend.yaml)

The workflow ensures successful building of the backend component and checks backend-specific unit tests.

Since the backend is a Kotlin project built with Gradle, 
the workflow should simply set up the necessary environment and delegate testing and building to Gradle. 

### [features.yaml](.github/workflows/features.yaml)

The workflow enforces the code style of the Feature Provider module,
ensures execution of basic scenarios with unit tests and verifies the database connectivity.

Along with the Python application, a postgres database is launched with credentials then relayed to the application.
The application must pass linter checks by `flake8` and all the tests provided in the module including successful connection to the database filled with the testing data.

### [web.yaml](.github/workflows/web.yaml)

The workflow enforces the code style of the Web module and checks its buildability. 

Since frontend is built by a system based on Node.js, the verification should be delegated to the `npm` tool.

### [integration-tests.yaml](.github/workflows/integration-tests.yaml)

The goals of the integration tests:
- Verify all the components can be easily brought online in a Docker container using `docker-compose`. 
- Check each component is reachable under the internal Docker network one-by-one. 
- Ensure the database credentials are set up correctly and the database is reachable as well.
- Backend and features provider are connected, and the requests are relayed correctly. 

Currently,
docker-compose is used to run the application, 
and simple requests targeting all components and specific backend endpoints are executed to check reachability.

Later verification of the connectivity between the frontend and backend should be added. 

## How do we work on it

Just like our project is split in three modules, our team is also split into three module-specific teams, who hold the knowledge and responsibility for their part. Each team has a representative for a single point of administration and management in the team. 

For each sprint, 1-3 representatives gather together (everyone else is also welcomed to meetings, however are not required), discuss current state and vision of the project among with tasks to be done this sprint, after which the specific, split tasks are formulated and published to the teams. Representatives also actively participate in resolving the tasks.

The tasks themselves are usually stored, assigned and manipulated in our canban board ("Projects" on GitHub), however the communication is done either in person or on a separate messaging platform.

