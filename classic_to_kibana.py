import datetime
import glob
import json
import os

import config
from default import DefaultClassicLog

class MissingLogfileError(Exception):
    pass

def get_log_data(fn):
    log_data = DefaultClassicLog(fn)
    log_data.data()
    log_data.parse()
    return log_data



def check_file_status(fn):
    if not os.path.isfile(fn):
        error = "\nFile not found: %s\nLog files NOT loaded.\nStopping execution at %s"%(fn,str(datetime.datetime.now()))
        raise MissingLogfileError(error) 



def get_most_recent_file(filedir):
    file_list = glob.glob(filedir)
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



# "Update Master" Log -- exclude bibcodes in progress (number == '000000')
def get_master_exclude():

# This is used to get metadata from the three update master logs.  The
# default operation will be to parse the messages into columns, and then
# return an enhanced dictionary including both the original message, and
# the parsed columns.  Alternatively, you could just bypass the parsing
# code and define records = update_master.records

    records = []
    files = [config.UPDATE_MASTER_AST,
             config.UPDATE_MASTER_PHY,
             config.UPDATE_MASTER_GEN]

    for fn in files:

        check_file_status(fn)
        update_master = get_log_data(fn)

        if config.DO_PARSE:
            logv_name = ['bibcode','bibfile','bibfile2','YYMM','number',
                         'database','timestamp','message']
            db = fn[20:23]
            for r in update_master.records:
                logv = r['error_msg'].split()
                logv.append(db)
                logv.append(r['timestamp'])
                logv.append(r['error_msg'])
                try:
                    logv[4]
                except IndexError:
                    print "End of file:%s"%fn
                else:
                    if(logv[4] == '000000'):
                        rec = dict(zip(logv_name, logv))
                        records.append(rec)
        else:
            records = update_master.records

    return records




# "DOI/FIXME" Log 
def doi_error_read():

    records = []

    fn = config.DOI_ERROR_LOG
    check_file_status(fn)
    doi_errors = get_log_data(fn)

    if config.DO_PARSE:
        logv_name = ['error_type','doi','timestamp','message']
        for r in doi_errors.records:
            logv = r['error_msg'].split()
            logv.append(r['timestamp'])
            logv.append(r['error_msg'])
            rec = dict(zip(logv_name, logv))
            records.append(rec)
    else:
        records = doi_errors.records

    return records



# "Bibcode duplicates" Log
def bibcode_dups_read():

    records = []

    fn = config.BIBCODE_DUPLICATE_LOG
    check_file_status(fn)
    bibcode_dups = get_log_data(fn)

    if config.DO_PARSE:
        logv_name = ['bibcode','bibcode2','timestamp','message']
        for r in bibcode_dups.records:
            logv = r['error_msg'].split()
            logv.append(r['timestamp'])
            logv.append(r['error_msg'])
            rec = dict(zip(logv_name, logv))
            records.append(rec)
    else:
        records = bibcode_dups.records

    return records



# "Update Citing" Log
def update_citing_read():

    records = []

    fn = get_most_recent_file(config.UPDATE_CITING_LOG)
    check_file_status(fn)
    update_citing = get_log_data(fn)

    if config.DO_PARSE:
        logv_name = ['bibcode', 'xmlfile', 'timestamp', 'message']
        for r in update_citing.records:
            logv = r['error_msg'].split()
            if len(logv) < 2:
                logv.append('')
            logv.append(r['timestamp'])
            logv.append(r['error_msg'])
            rec = dict(zip(logv_name, logv))
            records.append(rec)
    else:
        records = update_citing.records

    return records



def deleted_bibs_read():

    records = []

    files = [get_most_recent_file(config.DELETED_BIBS_AST),
             get_most_recent_file(config.DELETED_BIBS_PHY)]

    for fn in files:
        check_file_status(fn)
        deleted_bibs = get_log_data(fn)
        deleted_bibs_recs = [rec for rec in deleted_bibs.records if 'mkdeletedbibs' in rec['error_msg']]

        if config.DO_PARSE:
            for r in deleted_bibs_recs:
                logv_name = ['bibcode', 'database', 'timestamp', 'message']
                db = fn[20:23]
                lsplit = r['error_msg'].strip().split()
                logv = [lsplit[-1],db,r['timestamp'],r['error_msg']]
                rec = dict(zip(logv_name, logv))
                records.append(rec)
        else:
            records = deleted_bibs_recs

    return records




def make_kibana_records():

    doi_errs = doi_error_read()
    bibc_dups = bibcode_dups_read()
    update_citing = update_citing_read()
    deleted_bibs = deleted_bibs_read()

    if config.DO_PARSE and config.DO_EXCLUDE_IN_PROGRESS:
        exclude = get_master_exclude()
        bibcode_exclude = [rec['bibcode'] for rec in exclude]
        bibc_dups = filter_bibcodes(bibc_dups,bibcode_exclude)
        update_citing = filter_bibcodes(update_citing,bibcode_exclude)
        deleted_bibs = filter_bibcodes(deleted_bibs,bibcode_exclude)

    kibana_records = [{'logfile':'DOI-FIXME', 'records': doi_errs}, {'logfile': 'bibcodes.list.alt.dups', 'records': bibc_dups}, {'logfile': 'update_citing.bibs.manual', 'records': update_citing}, {'logfile': 'deleted_bibcodes', 'records': deleted_bibs}]

    return kibana_records



def main():


    recs = make_kibana_records()

    print json.dumps(recs, sort_keys = True, indent = 2)


if __name__ == '__main__':
    main()
