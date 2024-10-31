# grove_street
Welcome to Grove Street, Home.

## Project requirements

Running this project requires `Docker` to be installed (https://docs.docker.com/engine/install/).

## Running with docker

This project uses docker to create a container for the django project itself and a separate postgresql container that communicates with it.

In order to run docker build you need to define environment file for it.

Create a file called `.env.dev` in the project root, which is used to pass environment variables to development server.

Example configuration:

```
DEBUG=1
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_DB=<database name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=db # refers to database via docker network as defined in docker-compose.yml
POSTGRES_PORT=5432
```

After setting up `.env.dev` file you can build and run the project by running `docker compose up -d --build` command.

Development container automatically flushes the database and runs migrations when container is first created so the website should be up and running if no errors occured.

Website should be accessible at [https://localhost:8000/](https://localhost:8000/) and the container reacts to code changes in the local repository so it can be used for development as is.

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

## Running tests

You can run tests on docker container by running `docker-compose run web python manage.py test` command.

Running tests requires for the database user to have CREATEDB privilege.
If the user does not already have this privilege, alter the user to have it.

* Log into psql with postgresql user.
* Input following command for the desired DB user.

```
> ALTER USER <username> CREATDB;
```

Using this configuration you can attach to the docker container through port 3000. Note that this is only available in development and not in production.

## Test coverage

You can test test coverage using this https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py

## Running with docker in production

When deploying to production, this project uses docker to create a container for the django project itself, a separate postgresql container and nginx reverse proxy container.

In order to run docker production build you need to define environment file for it.

Create a file called `.env.prod` in the project root, which is used to pass environment variables to development server.

Example configuration:

```
DEBUG=0
SECRET_KEY=<generate new secret key>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 [::1]
POSTGRES_DB=<database name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=db # refers to database via docker network as defined in docker-compose.yml
POSTGRES_PORT=5432
```

After setting up `.env.prod` file you can build and run the project by running `docker-compose -f docker-compose.prod.yml up -d --build` command.

Afterwards you need to manually run the command for migration, as production server does not do it on the entrypoint script.
* Migrate database `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --noinput`
* Collect staticfiles `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`

Website should be accessible at [https://localhost:80/](https://localhost:80/).
