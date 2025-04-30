# TrackMyOffer

Look for the tasks in the "Projects" tab on github

For parts description look into the corresponding subdirectories.

## Run

### Docker

Put your API key in [FeaturesProvider/.env](FeaturesProvider/.env) (it won't work otherwise) and run 
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