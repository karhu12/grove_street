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
WAIT_FOR_DEBUGGER=0
SECRET_KEY=foo
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1
DJANGO_TRUSTED_ORIGINS=http://localhost http://127.0.0.1
POSTGRES_DB=<database name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=db # refers to database via docker network as defined in docker-compose.yml
POSTGRES_PORT=5432
```

After setting up `.env.dev` file you can build and run the project by running `docker compose up -d --build` command.

Afterwards you need to manually run the command for migration if not done before, as development server does not do it automatically.
* Migrate database `docker-compose exec web python manage.py migrate`

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

If you want debugger to wait for attach at the start, change the `WAIT_FOR_DEBUGGER` environment option in the `.env.dev` file

Using this configuration you can attach to the docker container through port 3000. Note that this is only available in development and not in production.

## Running tests

You can run tests on docker container by running `docker-compose exec web pytest` command.

Running tests requires for the database user to have CREATEDB privilege.
If the user does not already have this privilege, alter the user to have it.

* Log into psql with postgresql user.
* Input following command for the desired DB user.

```
> ALTER USER <username> CREATDB;
```

## Test coverage

You can test test coverage using this https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py¨

## Debugging test cases

Test cases can be debugged in a similar way to main project.

Copy the `launch.json` configuration attach debugging, and rename it. You only need to change port from `3000` to `3001`, which is test specific debugger port.

After the modification run the tests with the following modification `docker-compose exec web pytest --wait-for-debugger`. The test cases are not run until a debugger is attached on port `3001`.


## Running with docker in production

When deploying to production, this project uses docker to create a container for the django project itself, a separate postgresql container and nginx reverse proxy container.

In order to run docker production build you need to define environment file for it.

Create a file called `.env.prod` in the project root, which is used to pass environment variables to development server.

Example configuration:

```
DEBUG=0
WAIT_FOR_DEBUGGER=0
SECRET_KEY=<generate new secret key>
DJANGO_ALLOWED_HOSTS=localhost 127.0.0.1 <www domain name>
DJANGO_TRUSTED_ORIGINS=https://localhost https://127.0.0.1 https://<www domain name>
POSTGRES_DB=<database name>
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_HOST=db # refers to database via docker network as defined in docker-compose.yml
POSTGRES_PORT=5432
```

For the next step you need to set up your SSL certificates. In my case I am running cloudflare DNS which provides origin certificate files (certificate and private key).

Copy certificate and private key to `/etc/ssl/nginx` folder with the name `cert.pem` and `key.pem`.

After setting up SSL certificates and `.env.prod` file, you can build and run the project by running `docker-compose -f docker-compose.prod.yml up -d --build` command.

Afterwards you need to manually run the command for migration and collecting static files, as production server does not do it automatically.
* Migrate database `docker-compose -f docker-compose.prod.yml exec web python manage.py migrate --no-input`
* Collect static files `docker-compose -f docker-compose.prod.yml exec web python manage.py collectstatic --no-input --clear`

These commands should be run when ever there is new migration files added to the version control or new static files.

Website should be accessible at [https://localhost:443/](https://localhost:443/).
