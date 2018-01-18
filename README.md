# spyFront

# Running the application

MUST BE RUN ON A DOCKER HOST!!!

                  _     _                _                                      _            _                                    _     _
  /\/\  _   _ ___| |_  | |__   ___    __| | ___  _ __   ___    ___  _ __     __| | ___   ___| | _____ _ __   _ __ ___   __ _  ___| |__ (_)_ __   ___
 /    \| | | / __| __| | '_ \ / _ \  / _` |/ _ \| '_ \ / _ \  / _ \| '_ \   / _` |/ _ \ / __| |/ / _ \ '__| | '_ ` _ \ / _` |/ __| '_ \| | '_ \ / _ \
/ /\/\ \ |_| \__ \ |_  | |_) |  __/ | (_| | (_) | | | |  __/ | (_) | | | | | (_| | (_) | (__|   <  __/ |    | | | | | | (_| | (__| | | | | | | |  __/
\/    \/\__,_|___/\__| |_.__/ \___|  \__,_|\___/|_| |_|\___|  \___/|_| |_|  \__,_|\___/ \___|_|\_\___|_|    |_| |_| |_|\__,_|\___|_| |_|_|_| |_|\___|


              |<-------  docker containers  ----->|
+---------+   +----------+   +-------+   +--------+
|         |   |          |   |       |   |        |   
| OneView |<->| spymongo |-->|mongodb|<--|spyfront|
|         |   |          |   |       |   |        |
+---------+   +----------+   +-------+   +--------+
                 APP		        DB	        WEB

- Checkout code on https://github.com/xod442/spymfront.git save it on the /opt directory on your docker machine.

      - cd /opt
      - git clone https://github.com/xod442/spyfront.git
      - cd spyfront

spyFront is a graphical utility for viewing the mongo database entries from spymongo.

Point the web browser at the docker host on port 5003 ex. 10.10.10.10:5003

Application is containerized to run in docker

from the spyfront directory on you docker host, you will need to build the docker container
type: 'docker build -t spyfront .'     (copy everything inside the quotes...even the dot)

The database container has to be up prior to starting the spyfront image
- Start mongodb separately: `docker run --name spy-db -d mongo` (This will start the mongo database)
- Start/Link the app: `docker run --name spyfront --link spy-db:mongo -p 5003:5003 -d spyfront python manage.py runserver`
