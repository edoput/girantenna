Girantenna
----------

A joyful web interface to rotate your community network node's antennas

Permissions
-----------

The server must have access to the GPIO pins so the user running it
should belong to `gpio` group.

Development
----------

```
source development
flask run
```

Deploy
------

Either place a reverse proxy in front of the app running or pass requests with a WSGI compatible web server. 

#### Reverse proxy

With a reverse proxy there are two processes (reverse proxy and server), make sure the server belong to the group `gpio`.
