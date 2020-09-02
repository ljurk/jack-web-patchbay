# jack_web

This script starts a webserver and serves an interface to patch jack connections

## installation

```
$ pip install jack_web
```

## usage

start the server
```
$ jack_web
```
the webinterface can be accessed on this page http://localhost:2323/

## editing html & css

first: find the directory in which your package is installed
```
$ pip show jack_web | grep Location
```

append `jack_web/templates/index.html`

in my case `/home/ljurk/.local/lib/python3.8/site-packages/jack_web/templates/index.html`
