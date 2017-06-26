## Websocket Site Analytics

### Goal:

Create a real time analytics platform which communicates to the main server VIA web socket on events.

Data is then aggregated and displayed VIA REST API in the dashboard.

Goals include testing the limitations of websockets sending large numbers of requests, and potential issues with database writes.

Each websocket write is about 2000 characters, and there can be upwards of 20 events/user/second.


### Install/Setup:

This project is meant to be run on a server with docker-compose. See github repo kburts/kevinsapps.com for example docker-compose file.

Note an analytics/.env file is required

#### Oauth:

Make sure to add a Social application for Reddit in the admin if Reddit login is needed.


### Testing:

`python manage.py test`

