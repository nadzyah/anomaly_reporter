from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import datetime
from bson.json_util import dumps
import json

from st2common.runners.base_action import Action

class GetAnomalyLogsAction(Action):

    def run(self, mongouri, sourcedb, cols_and_hosts, event_handler_period,
            hostname_index, datetime_index, message_index):
        """ Return dict with the format
        { hostname1: [list of logs]
          hostname2: [list of logs] }

        Cols_and_host defines the collections where the logs for specific hostnames are stored
        The format:
        { collection1: [list of hostnames],
          collection2: [list of hostnames]
        }
        """

        connection = MongoClient(mongouri)
        db = connection[sourcedb]
        now = datetime.datetime.now()
        result = {}

        for col, hosts in cols_and_hosts.items():
            mg_col = db[col]
            for host in hosts:
                query = {
                    datetime_index: {
                        '$gte': now - datetime.timedelta(days=event_handler_period),
                        '$lt': now
                    },
                    hostname_index: host
                }
                data = dumps(mg_col.find(query).sort(datetime_index, -1))
                json_data = json.loads(data)

                result[host] = [x[message_index] for x in json_data]

        connection.close()
        return (True, result)
