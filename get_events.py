#!/usr/bin/env python
#
# Fetch event (earthquake) information from the catalogs submitted to the IRIS DMC.
#
# Author: Mijian Xu, Tao Gou @ Nanjing University
#
# History: 2016-05-03, Init code, Mijian Xu
#          2016-05-07, Create opt function, Tao Gou
#          2016-06-02, Modify date and time options, Mijian Xu
#

import sys
import getopt
from util import Events, get_time
from datetime import datetime
try:
    import urllib.request as rq
except:
    import urllib as rq

def Usage():
    print("Usage: get_events.py -Yminyear/minmonth/minday/maxyear/maxmonth/maxday [-Rminlon/maxlon/minlat/maxlon]\n"
          "\t[-Dcenterlat/centerlon/minradius/maxradius] [-Hmindepth/maxdepth] [-Mminmag/maxmag[/magtype]] [-cCatalog] [-stime|mag]")
    print("-C -- If -C specified results should not include station and channel comments.")
    print("-D -- RADIAL search terms (incompatible with the box search)")
    print("-H -- Limit to events with depth between this range.")
    print("-M -- Limit to events with magnitude between this range.\n\
            Specify magnitude type e.g., ML, Ms, mb, Mw")
    print("-R -- BOX search terms (incompatible with radial search)")
    print("-b -- Limit to events occurring on or after the specified start time.")
    print("-c -- Specify the catalog from which origins and magnitudes will be retrieved.\n\
            avaliable catalogs: ANF, GCMT, ISC, UoFW, NEIC")
    print("-e -- Limit to events occurring on or before the specified end time.")
    print("-s -- Order results by \"time\" or \"magnitude\", (\"time\" is default).")

def opt():
    lalo_label = ''
    dep_label = ''
    date_label = ''
    mag_label = ''
    sort_label = ''
    cata_label = ''
    iscomment = True
    try:
        opts, args = getopt.getopt(sys.argv[1:], "R:D:b:e:c:H:M:s:C")
    except:
        print("Invalid arguments")
        Usage()
        sys.exit(1)
    if sys.argv[1:] == []:
        print("No argument is found")
        Usage()
        sys.exit(1)
    if not ("-b" in [op for op, value in opts] and "-e" in [op for op, value in opts]):
        print("\"-b\" and \"-e\" must be specified.")
        sys.exit(1)

    for op, value in opts:
        if op == "-R":
            lon1 = value.split("/")[0]
            lon2 = value.split("/")[1]
            lat1 = value.split("/")[2]
            lat2 = value.split("/")[3]
            lalo_label = 'minlat='+lat1+'&maxlat='+lat2+'&minlon='+lon1+'&maxlon='+lon2+'&'
        elif op == "-D":
            lat = value.split("/")[0]
            lon = value.split("/")[1]
            dist1 = value.split("/")[2]
            dist2 = value.split("/")[3]
            lalo_label ='lat='+lat+'&lon='+lon+'&maxradius='+dist2+'&minradius='+dist1+'&'
        elif op == "-H":
            dep1 = value.strip("/")[0]
            dep2 = value.strip("/")[1]
            dep_label = 'mindepth='+dep1+'&maxdepth='+dep2+'&'
        elif op == "-b":
            begintime = get_time(value)
        elif op == "-e":
            endtime = get_time(value)
        elif op == "-c":
            cata_label = 'catalog='+value+'&'
        elif op == "-M":
            mag1 = value.split("/")[0]
            mag2 = value.split("/")[1]
            if len(value.split("/")) == 2:
                mag_label = 'minmag='+mag1+'&maxmag='+mag2+'&'
            else:
                mtype = value.split("/")[2]
                mag_label = 'minmag='+mag1+'&maxmag='+mag2+'&magtype='+mtype+'&'
        elif op == "-s":
            if value.lower() == 'mag':
                sort_label = 'orderby=magnitude'+'&'
            elif value.lower() == 'time':
                sort_label = ''
            else:
                print("Wrong option of \"-s\"")
                sys.exit(1)
        elif op == "-C":
            iscomment = False
        else:
            print("Invalid arguments")
            Usage()
            sys.exit(1)
    date_label = "start="+begintime.strftime("%Y-%m-%dT%H:%M:%S")+\
                 "&end="+endtime.strftime("%Y-%m-%dT%H:%M:%S")+"&"
    return lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment

def main():
    lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment = opt()
    events = Events(lalo_label, dep_label, mag_label, cata_label, date_label, sort_label, iscomment)
    events.download()
    events.output()

if __name__ == '__main__':
    main()
