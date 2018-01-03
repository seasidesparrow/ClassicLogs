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

    args=parser.parse_args()
    return args



def main():

    args = get_arguments()


    if args.diag:
        records = ['test']

    else:
        records = make_kibana_records()

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
