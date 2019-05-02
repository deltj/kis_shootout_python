#!/usr/bin/env python3

import argparse
from enum import Enum
import getpass
import sys
import time

import KismetRest

# Current program state. Syncing means we're waiting for cards to be tuned to
# the specified channel, Collecting means the cards are tuned and we're counting
# frames
class State(Enum):
    Syncing = 1,
    Collecting = 2

# This object stores information about a data source we're tracking
class SourceInfo:
    name = ""       # The name of this data source
    uuid = 0        # Kismet's UUID for this data source
    chan = 0        # The channel this data source is tuned to
    count = 0       # The number of frames observed by this data source
    offset = 0      # Frame count offset (to account for sync time)

uri = "http://localhost:2501"

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Kismet 802.11 datasource shootout")
    parser.add_argument("sources", metavar="source", nargs="+",
            help="data sources to use in the shootout")
    parser.add_argument("-c", dest="channel", type=int, required=True,
            help="the channel to monitor")
    parser.add_argument("-u", dest="user",
            help="a user name to log into Kismet with")
    parser.add_argument("-p", dest="ask_for_password", action="store_true",
            help="tells this program to prompt for a password")

    # Process command-line arguments
    args = parser.parse_args()

    username = ""
    if args.user:
        username = args.user

    password = ""
    if args.ask_for_password:
        password = getpass.getpass()

    sources_by_name = dict()
    for source_name in args.sources:
        si = SourceInfo()
        si.name = source_name
        sources_by_name[source_name] = si

    if len(sources_by_name) < 2:
        print("A shootout with only one data source is uninteresting, but whatever...")

    # Connect to Kismet
    kr = KismetRest.KismetConnector(uri)
    #kr.set_debug(True)
    kr.set_login(username, password)

    if not kr.check_session():
        print("Invalid login")
        sys.exit(1)

    # Update data source UUIDs
    datasources = kr.datasources()
    for source_name, source in sources_by_name.items():
        for ds in datasources:
            if ds['kismet.datasource.name'] == source.name:
                source.uuid = ds['kismet.datasource.uuid']
        if source.uuid == 0:
            print("Kismet doesn't have a source named {}".format(source.name))
            sys.exit(0)

    # Set channel for specified data sources
    state = State.Syncing
    print("Tuning data sources to channel {}".format(args.channel))
    for source_name, source in sources_by_name.items():
        print("uuid: {}, channel: {}".format(source.uuid, args.channel))
        fart = kr.config_datasource_set_channel(source.uuid, str(args.channel))
        print(fart)

    counts = dict()

    while True:
        datasources = kr.datasources()

        if state == State.Syncing:
            # TODO:Wait for data sources to all be on the same channel
    
            # Update packet counter offsets
            for ds in datasources:
                ds_name = ds['kismet.datasource.name']
                sources_by_name[ds_name].offset = ds['kismet.datasource.num_packets']
                print("Offset for {} = {}".format(ds_name, sources_by_name[ds_name].offset))

            state = State.Collecting
            
        elif state == State.Collecting:
            # Update packet counters
            for ds in datasources:
                ds_name = ds['kismet.datasource.name']
                counts[ds_name] = ds['kismet.datasource.num_packets'] - sources_by_name[ds_name].offset

            max_count = max(counts.values())
            if max_count == 0: max_count = 1

            for ifc, count in counts.items():
                print("{} {} ({:.2%})".format(ifc, count, count / max_count))

        else:
            print("State error")
            sys.exit(1)

        time.sleep(1)

