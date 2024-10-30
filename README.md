# grove_street
Welcome to Grove Street, Home.


## Running development server with docker

To start a development server run `docker compose up -d --build` command.

## Running produciton server with docker

To start a production server run `docker-compose -f docker-compose.prod.yml up -d --build` command.

Afterwards you need to manually run the command for migration, as production server does not do it on the entrypoint script.

Migrate database: `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`

Collect staticfiles: `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`

## VSCode debugging setup

You can setup debugging with visual studio code by copying this configuration to `/.vscode/launch.json` (create this path and file if it does not exist).

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Django attach",
            "type": "debugpy",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 3000
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": ".."
                }
            ]
        },
    ]
}
```

Using this configuration you can attach to the docker container through port 3000. Note that this is only available in development and not in production.

## Test coverage

You can test test coverage using this https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py

## Running tests

You can run tests by using the manage.py inside the grove_street folder `python manage.py test`.


Running tests requires for the database user to have CREATEDB privilege.
If the user does not already have this privilege, alter the user to have it.

* Log into psql with postgresql user.
* Input following command for the desired DB user.

```
> ALTER USER <username> CREATDB;
```