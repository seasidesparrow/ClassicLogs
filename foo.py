import json
from default import DefaultClassicLog
import config


# Update Master Log

def get_log_data(fn):
    log_data = DefaultClassicLog(fn)
    log_data.data()
    log_data.parse()
    return log_data

def get_master_exclude():

    records = []
    files = [config.UPDATE_MASTER_AST,
             config.UPDATE_MASTER_PHY,
             config.UPDATE_MASTER_GEN]

    logv_name = ['bibcode','bibfile','bibfile2',
                 'number','database','timestamp']

    for fn in files:
        db = fn[20:23]
        update_master = get_log_data(fn)
        for r in update_master.records:
            logv = r['error_msg'].split()
            if(logv[4] == '000000':
                logv[4] = None
                logv.append(db, r['timestamp'])
                rec = {logv_name[i]: logv[i]} for i in range(len(logv))
#               rec = {logv_name[0]: logv[0], logv_name[1]: logv[1], 
#                      logv_name[2]: logv[2], logv_name[3]: logv[3], 
#                      'database': db, 'timestamp': r['timestamp']}
                records.append(rec)

#       print json.dumps(records, sort_keys = True, indent = 4)
