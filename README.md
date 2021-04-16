Postgresql database implementation that stores information about writers and their works and a flask service to get data from the database.


Run via docker.
1) Clone this repo;
2) Fill database.ini file with your information;
3) Change arg "--init" in Dockerfile;
4) Run ./build in your repo dir.

Run via terminal.
1) Clone this repo;
2) Fill database.ini file with your information;
3.1) First running: "python3 app.py --init=True" for initial database;
3.2) Subsequent running "python3 app.py" for just lunch service.
