#!/usr/bin/env python

import config.config as cfg
import gzip
import os
import sys
from glob import glob
from parsers.arxiv import ArxivParser
from serializers.serializer_mp import ArxivToMasterPipeline

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







        print "\n\nBEGIN send parsed records to Master Pipeline ...\n\n"
        for r in parsed_records:
            if args.parse_only:
                print ("\n"+str(r)+"\n")
            else:
                mpsender=ArxivToMasterPipeline()
                mpsender.serialize(r)

    print "DONE."
    return


if __name__ == '__main__':
    main()
