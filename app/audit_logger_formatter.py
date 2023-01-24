import json
import logging

def get_access_log(record):
    json_obj = {'audit': {'log': {
        'level': record.levelname,
        'type': 'access',
        'timestamp': record.asctime,
        'message': record.message},
        'req': record.extra_info['req'],
        'res': record.extra_info['res']}}
    return json_obj

class CustomFormatter(logging.Formatter):

    def __init__(self, formatter):
        logging.Formatter.__init__(self, formatter)

    def format(self, record):
        logging.Formatter.format(self, record)
        return json.dumps(get_access_log(record), indent=2)
