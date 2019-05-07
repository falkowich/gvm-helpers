import csv
import xmltodict
from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print
from config import GVM_HOSTNAME, GVM_PORT, GVM_TIMEOUT, GVM_USER, GVM_PASSWD

connection = TLSConnection(hostname=GVM_HOSTNAME, port=GVM_PORT, timeout=GVM_TIMEOUT)
gmp = Gmp(connection = connection)


with open('targets.csv') as f:
    targets = list(csv.DictReader(f, delimiter=';'))
 
with gmp:
    gmp.authenticate(GVM_USER, GVM_PASSWD)

    xml_creds = gmp.get_credentials()
    dict_creds = xmltodict.parse(xml_creds)
    creds = dict_creds['get_credentials_response']['credential']
    credentials = {}
    for cred in creds:
        credentials[cred['name']]=cred['@id']

    for target in targets:
        result = gmp.create_target(
            name=target['name'], 
            hosts=[target['net']], 
            exclude_hosts=[target['exclude']], 
            comment=target['comment'],
            ssh_credential_id=credentials.get(target['ssh']),
            smb_credential_id=credentials.get(target['smb'])
            )
        print(result)