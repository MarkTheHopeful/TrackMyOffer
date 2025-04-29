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

### Script

To run all three services together, try out [run_local.sh](run_local.sh) script. Ensure to:
- put your model API key at the top of the script
- install all the requirements for all three parts separately

Logs from services will be available in `logs` directory