# TrackMyOffer

Look for the tasks in the "Projects" tab on github

For parts description look into the corresponding subdirectories.

## Requirements & Architecture 

- The Requirements Book for the project is available via this [link](https://docs.google.com/document/d/1xXU2xOTpktsWVINS9sxt_Pv6vnwDQvh9NQTqpTrnQbo/edit?usp=sharing). 
- The high-level architecture diagram is available via this [link](https://drive.google.com/file/d/1jBHv_NsWErqjyx7iRrGBuINruEsCgRWE/view?usp=sharing).
  - A document with reasoning behind the chosen architecture design is available via this [link](https://docs.google.com/document/d/1OYZI9EdXdObnDyrL7oCGbjBhDP-Oa-lCwMkZBPdz6ZA/edit?usp=sharing).

## Run

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