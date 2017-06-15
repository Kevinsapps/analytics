## Websocket Site Analytics

### Goal:

Create a really analytics platform which communicates to the main server VIA web socket on events.

Data is then aggregated and displayed VIA REST API in the dashboard.


### Install/Setup:

This project is meant to be run on a server with docker-compose. See github repo kburts/kevinsapps.com for example docker-compose file.

Note an analytics/.env file is required


### Testing:

python manage.py test