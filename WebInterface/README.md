## Web Interface

This part is responsible for web interface of the project, duh.

Q: What is it going to be?
A: A web interface to our service

Q: What the design is going to be?
A: To come up with a design is currently one of the tasks.

Q: Which parts does the interface communicate to?
A: Web Interface communicates directly with the Back End (specifically, its request dispatcher) and the external auth provider.

Q: Does it need direct communication to the Features Provider?
A: No! All communications are proxied with the Back End.

Q: What approximately should be in the interface?
A: Main answer: everything that needs to get the service provided. Detailed answer:
1. A login screen, duh. Probably we externalize the auth to something like OAuth.
2. <TBA>

Q: How should we do it? Which language/framework/whatever?
A: You are free to choose! If you have no ideas, then idk, React? HTML+CSS+JS? Flask???

Btw, after you decide on the language of your choice, don't forget to update .gitignore, otherwise we'll have to deal with .idea and stuff in the repo.

### Running frontend
1. Install `npm`
2. Change directory to a `WebInterface`.
3. Run `npm install`
4. Then for local run of frontend use `npm run dev`
5. For specifying host and port of backend (by default `localhost:8080`) use `VITE_API_HOST=0.0.0.0 VITE_API_PORT=8081 npm run dev`
6. For specifying host and port of frontend (by default `localhost:5173`) use `VITE_DEV_HOST=0.0.0.0 VITE_DEV_PORT=5000 npm run dev`