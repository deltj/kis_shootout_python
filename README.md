# kis_shootout_python
Kismet WiFi data source shootout implementation in Python3.

This program compares the received packet counters from multiple Kismet datasources.

```
usage: shootout.py [-h] -c CHANNEL [-u USER] [-p] SRC [SRC ...]

Kismet datasource shootout

positional arguments:
  SRC         data sources to use in the shootout (e.g. wlan0)

optional arguments:
  -h, --help  show this help message and exit
  -c CHANNEL  the channel to monitor
  -u USER     a user name to log into Kismet with
  -p          tells this program to prompt for a password
```

I run it like this: `./shootout.py -u kismet -p -c 8 alfa3 alfa4`
