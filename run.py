#!/usr/bin/env python

from config import config
import gzip
import os
import sys
from glob import glob
from classiclogs import make_kibana_records
import json

def get_arguments():

    import argparse

    parser=argparse.ArgumentParser(description='Command line options.')

    parser.add_argument('-d',
                        '--diagnose',
                        dest = 'diag',
                        action = 'store_true',
                        help = 'Send one test record to kibana')

    parser.add_argument('-s',
                        '--sample',
                        dest = 'sample',
                        action = 'store_true',
                        help = 'Send a snippet of each log instead of the full log')

    args=parser.parse_args()
    return args



def main():

    args = get_arguments()


    if args.diag:
        records = ['test']

    else:
        records = make_kibana_records()

    if args.sample:
        rec_temp = []
        for r in records:
            logfile = r['logfile']
            sample = []
            for i in range(5):
                sample.append(r['records'][i])
            rec_temp.append({'logfile': logfile, 'records': sample})
        records = rec_temp
                

    print json.dumps(records, sort_keys = True, indent = 2)





#       print "\n\nBEGIN send parsed records to Master Pipeline ...\n\n"
#       for r in parsed_records:
#           if args.parse_only:
#               print ("\n"+str(r)+"\n")
#           else:
#               mpsender=...
#               mpsender.serialize(r)

    return


if __name__ == '__main__':
    main()
