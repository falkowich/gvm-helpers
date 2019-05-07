import csv
from gvm.connections import TLSConnection
from gvm.protocols.latest import Gmp
from gvm.xml import pretty_print
from config import GVM_HOSTNAME, GVM_PORT, GVM_TIMEOUT, GVM_USER, GVM_PASSWD

connection = TLSConnection(hostname=GVM_HOSTNAME, port=GVM_PORT, timeout=GVM_TIMEOUT)
gmp = Gmp(connection = connection)

with gmp:
    gmp.authenticate(GVM_USER, GVM_PASSWD)

    credentials = gmp.get_credentials()
    print(credentials)    
