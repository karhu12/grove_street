# grove_street
Welcome to Grove Street, Home.

## Database setup (Windows)

* Create a file called `.env` to `/grove_street/`.
* Modify the contents to be as follows:

```
DEBUG=True (use False for production)
POSTGRES_USER=<user>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=<db name>
POSTGRES_PORT=<port number>
POSTGRES_HOST=<host address>
```

* .env file is loaded automatically using django-dotenv.


You should be able to use the database now.

## Running server

You can run the server by using the manager.py inside the grove_street folder `python manage.py runserver`.


## Running tests

You can run tests by using the manage.py inside the grove_street folder `python manage.py test`.


Running tests requires for the database user to have CREATEDB privilege.
If the user does not already have this privilege, alter the user to have it.

* Log into psql with postgresql user.
* Input following command for the desired DB user.

```
> ALTER USER <username> CREATDB;
```

## VSCode debugging setup

You can setup debugging with visual studio by copying this configuration to `/.vscode/launch.json` (create this path and file if they don't exist).

```
{
    // Use IntelliSense to learn about possible attributes.
    // Hover to view descriptions of existing attributes.
    // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
    "version": "0.2.0",
    "configurations": [
        {
          "name": "Python Debugger: Django runserver",
          "type": "debugpy",
          "request": "launch",
          "program": "manage.py",
          "cwd": "${workspaceFolder}\\grove_street",
          "args": ["runserver"],
          "django": true,
          "justMyCode": true
        },
        {
            "name": "Python Debugger: Django test",
            "type": "debugpy",
            "request": "launch",
            "program": "manage.py",
            "cwd": "${workspaceFolder}\\grove_street",
            "args": ["test", "--noinput"],
            "django": true,
            "justMyCode": true
          }
    ]
}
```

If you don't have `debugpy` extension, install it.

## Test coverage

You can test test coverage using this https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py