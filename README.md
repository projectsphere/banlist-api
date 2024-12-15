# Palworld Banlist API
 Create a Global Ban List API for managing bans across all your Palworld servers. This API will allow you to add, remove, and query bans efficiently.

 This API will be directly tied to [Sphere](https://github.com/projectsphere/sphere) discord bot for Palworld.

## Documentation
 - `/docs`: API Documentation and endpoints.

## Endpoints
 - `/api/banuser`: Endpoint allowing you to post a ban to the database.
 - `/api/unbanuser`: Endpoint allowing you to remove a ban from the database.
 - `/api/banlist.txt`: Endpoint that will be used in your `PalworldSettings.ini`.
 - `/api/bannedusers`: Endpoint that will output a full list of banned users displaying name, user id, and reason.
 - `/api/syncbans`: Endpoint that will pull Palworlds official banlist and add it to the database.

 ## Setup
 Simple setup for Docker.
 ```
 docker-compose up --build
 ```