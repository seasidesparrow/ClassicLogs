import os
import json
import datetime

import config
from default import DefaultClassicLog

def get_log_data(fn):
    log_data = DefaultClassicLog(fn)
    log_data.data()
    log_data.parse()
    return log_data

def verify_config():
    config_vars = globals().get('config')
    config_files = {key: value for key, value in config_vars.__dict__.iteritems() if not key.startswith('_')}
    for f in config_files.keys():
        if os.path.isfile(f):
            print "lol.",config_files[f]
        else:
            print "File not found, stopping:",config_files[f]
            print "Log files NOT loaded -- check filenames in config.py"
            print str(datetime.datetime.now())
            print quit()

# "Update Master" Log
def get_master_exclude():

    records = []
    files = [config.UPDATE_MASTER_AST,
             config.UPDATE_MASTER_PHY,
             config.UPDATE_MASTER_GEN]

    logv_name = ['bibcode','bibfile','bibfile2',
                 'number','database','timestamp','message']

    for fn in files:
        db = fn[20:23]
        update_master = get_log_data(fn)
        for r in update_master.records:
            logv = r['error_msg'].split()
            if(logv[4] == '000000'):
                logv[4] = None
                logv.append(db, r['timestamp'],r['error_mesg'])
                rec = dict(zip(logv_name, logv))
                records.append(rec)


def main():

    verify_config()

    records = get_master_exclude()

    print json.dumps(records, sort_keys = True, indent = 2)


if __name__ == '__main__':
    main()
