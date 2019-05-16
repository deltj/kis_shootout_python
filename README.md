# kis_shootout_python

A (new) Kismet WiFi data source shootout implementation in Python3, using the KismetRest library. 

The program displays PPS, total packets received, and the relative percentage of packets received for each datasource that has been specified. Output is updated once per second until the program is killed with CTRL+C.

```
Data Source    PPS     Packets        RX %
------------------------------------------
alfa3          433        2133      98.61%
alfa4          416        2163     100.00%
tplink1        288        1383      63.94%
alfa1           66         373      17.24%
alfa2           57         237      10.96%

Elapsed time: 0 Hours 0 Minutes 5 Seconds
```

## Background

A person interested in using 802.11 interfaces in monitor mode may also be interested in comparing the frame-receiving performance of various 802.11 adaptors. This program is intended to facilitate this kind of testing, as described here: https://wirelessctf.blogspot.com/2018/05/new-wifi-card-testing-kismetshootout.html

This program is a rewrite of kismet_shootout.rb in Python3. The original Ruby implementation (available here: https://github.com/kismetwireless/kismet/blob/Kismet-Stable/ruby/kismet_shootout.rb) only works with "old" kismet. This python rewrite works with the "new" kismet.

## Usage

```
usage: shootout [-h] -c CHANNEL [-u USER] [-p] SRC [SRC ...]

Kismet datasource shootout

positional arguments:
  SRC         data sources to use in the shootout (e.g. wlan0)

optional arguments:
  -h, --help  show this help message and exit
  -c CHANNEL  the channel to monitor
  -u USER     a user name to log into Kismet with
  -p          tells this program to prompt for a password
  ```

I run it like this: `./shootout -u kismet -p -c 8 alfa3 alfa4`

