#!/usr/bin/env python

from config import config
import gzip
import os
import sys
from glob import glob
from classiclogs import make_kibana_records
import json
#from serializers.serializer_mp import ArxivToMasterPipeline

def get_arguments():

    import argparse

    parser=argparse.ArgumentParser(description='Command line options.')

    parser.add_argument('-d',
                        '--diagnose',
                        dest = 'diag',
                        action = 'store_true',
                        help = 'Send one test ArXiv record to the pipeline')

    args=parser.parse_args()
    return args



def main():

    args = get_arguments()


    test = make_kibana_records()

    print json.dumps(test, sort_keys = True, indent = 2)







#       print "\n\nBEGIN send parsed records to Master Pipeline ...\n\n"
#       for r in parsed_records:
#           if args.parse_only:
#               print ("\n"+str(r)+"\n")
#           else:
#               mpsender=ArxivToMasterPipeline()
#               mpsender.serialize(r)

    return


if __name__ == '__main__':
    main()
