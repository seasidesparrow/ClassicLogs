#!/usr/bin/env python

import json
import datetime
import os
import glob
import config


def get_most_recent_file(filedir):

    file_list = glob.glob(filedir+'*')

    try:

        most_recent_file = max(file_list, key = os.path.getctime)

    except ValueError:

        print "Could not find list of files: ",filedir
        most_recent_file = ''

    else:

        pass

    return most_recent_file



def filter_bibcodes(input_list,exclude_list):

    output_list = [rec for rec in input_list if rec['bibcode'] not in exclude_list]

    return output_list



def get_master_exclude():

    records = []

    files=[config.UPDATE_MASTER_AST,
                 config.UPDATE_MASTER_PHY,
                 config.UPDATE_MASTER_GEN]

    for f in files:

        try:
            write_time = str(datetime.datetime.fromtimestamp(os.path.getmtime(f)))
        except OSError:

            print "UPDATE_MASTER file not found:",f

        else:

            with open(f) as fp:
                db = f[20:23]
                for line in fp.readlines():
                    bibc, bibf, bibf2, num, date = line.strip().split()
                    read_time = str(datetime.datetime.utcnow())
                    if str(date) == '000000':
                        rec = {'bibcode': bibc, 'bibfile': bibf, 'bibfile2': bibf2, 'number': num, 'database': db, 'timestamp_read': read_time, 'timestamp_write': write_time}
                        records.append(rec)

    return records



def doi_error_read():

    records = []

    try:
        write_time = str(datetime.datetime.fromtimestamp(os.path.getmtime(config.DOI_ERROR_LOG)))

    except OSError:

        print "DOI_ERROR_LOG not found:",config.DOI_ERROR_LOG

    else:

        with open(config.DOI_ERROR_LOG) as fp:

            for line in fp.readlines():
                error, doi = line.strip().split()
                rec = dict()
                read_time = str(datetime.datetime.utcnow())
                rec = {'error_type': error, 'error_msg': doi, 'timestamp_read': read_time, 'timestamp_write': write_time}
                records.append(rec)

    return records



def bibcode_dups_read():

    records = []

    try:
        write_time = str(datetime.datetime.fromtimestamp(os.path.getmtime(config.BIBCODE_DUPLICATE_LOG)))

    except OSError:

        print "BIBCODE_DUPLICATE_LOG not found:",config.BIBCODE_DUPLICATE_LOG

    else:
        with open(config.BIBCODE_DUPLICATE_LOG) as fp:
            for line in fp.readlines():
                rec = dict()
                bibc1, bibc2 = line.strip().split()
                read_time = str(datetime.datetime.utcnow())
                rec = {'bibcode': bibc1, 'bibcode_2': bibc2, 'timestamp_read': read_time, 'timestamp_write': write_time}
                records.append(rec)

    return records



def update_citing_read():

    records = []

    filename = get_most_recent_file(config.UPDATE_CITING_LOG)

    try:
        write_time = str(datetime.datetime.fromtimestamp(os.path.getmtime(filename)))

    except OSError:

        print "UPDATE_CITING_LOG not found:",config.UPDATE_CITING_LOG

    else:

        with open(filename) as fp:
            for line in fp.readlines():
                rec = dict()
                try:
                    bibcode, xmlfile = line.strip().split()
                except ValueError:
                    bibcode = line.strip()
                    xmlfile = None
                else:
                    pass
                read_time = str(datetime.datetime.utcnow())
                rec = {'bibcode': bibcode, 'xmlfile': xmlfile, 'timestamp_read': read_time, 'timestamp_write': write_time}
                records.append(rec)

    return records



def deleted_bibs_read():

    records = []

    files = [get_most_recent_file(config.DELETED_BIBS_AST), 
             get_most_recent_file(config.DELETED_BIBS_PHY)]

    for filename in files:

        try:

            write_time = str(datetime.datetime.fromtimestamp(os.path.getmtime(filename)))

        except OSError:

            print "DELETED_BIBS file not found:",filename

        else:

            with open(filename) as fp:
                db = filename[20:23]
                for line in fp.readlines():
                    if 'mkdeletedbibs' in line:
                        rec = dict()
                        lsplit=line.strip().split()
                        read_time = str(datetime.datetime.utcnow())
                        rec = {'bibcode': lsplit[-1], 'database': db, 'error_msg': line.strip(), 'timestamp_read': read_time, 'timestamp_write': write_time}
                        records.append(rec)

    return records



def make_kibana_records():

    exclude = get_master_exclude()
    bibcode_exclude = [rec['bibcode'] for rec in exclude]

    doi_errs = doi_error_read()

    bibc_dups = filter_bibcodes(bibcode_dups_read(),bibcode_exclude)

    update_cites = filter_bibcodes(update_citing_read(),bibcode_exclude)

    deleted_bibs = filter_bibcodes(deleted_bibs_read(),bibcode_exclude)

    kibana_records = [{'logfile':'DOI-FIXME', 'records': doi_errs}, {'logfile': 'bibcodes.list.alt.dups', 'records': bibc_dups}, {'logfile': 'update_citing.bibs.manual', 'records': update_cites}, {'logfile': 'deleted_bibcodes', 'records': deleted_bibs}]

    return kibana_records



def main():

    recs = make_kibana_records()

    print json.dumps(recs, sort_keys = True, indent = 4)


if __name__ == '__main__':
    main()
