# grove_street
Welcome to Grove Street, Home.

## Database setup (Windows)

* Add `.pg_service.conf` file to `%APPDATA%/postgresql/` (create this directory if it does not exist).
* Modify the contents to be as follows:

```
[grove_street]
host=<host address>
user=<database username>
dbname=<database name>
port=<port number>
password=<database user password>
```
