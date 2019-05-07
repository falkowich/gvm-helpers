import csv
import xmltodict
from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.xml import pretty_print
from config import GVM_HOSTNAME, GVM_PORT, GVM_TIMEOUT, GVM_USER, GVM_PASSWD

connection = TLSConnection(hostname=GVM_HOSTNAME, port=GVM_PORT, timeout=GVM_TIMEOUT)
gmp = Gmp(connection = connection)

with open('tasks.csv') as f:
    tasks = list(csv.DictReader(f, delimiter=';'))

with gmp:
    gmp.authenticate(GVM_USER, GVM_PASSWD)

    xmlt = gmp.get_targets()
    t = xmltodict.parse(xmlt)
    xt = t['get_targets_response']['target']
 
    targets = {}
    for target in xt:
        targets[target['name']]=target['@id']

    for task in tasks:
        result = gmp.create_task(
            name=task['name'], 
            config_id=task['config_id'], 
            target_id=targets.get(task['target']), 
            scanner_id=task['scanner_id'],
            comment=task['comment'],
            alterable=task['alterable'],
            schedule_id=task['schedule_id']
            )
        print(result)