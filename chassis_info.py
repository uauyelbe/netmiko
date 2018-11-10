from jnpr.junos import Device
from jnpr.junos.exception import ConnectError
from jnpr.junos.op.inventory import ModuleTable
import pandas as pd
from pandas import ExcelWriter
from pprint import pprint
from easygui import passwordbox
from xml.dom import minidom
from lxml import etree
import xml.etree.ElementTree as ET
import sys

psw = passwordbox("password: ")
def connect(host):
    dev = Device(host=host, user="uauyelbekov", password=psw)
    return dev

def get_info():
    devices = list()
    pem_name = list()
    pem_serial = list()
    pem_state = list()
    with open("devices/bngmx.txt", "r") as bngmx:
        bngmx = bngmx.readlines()
        for host in bngmx:
            devices.append(host.strip())
            dev = connect(host.strip())
            try:
                dev.open()
                print("result for host " + host)
            except ConnectError as err:
                print("cannot connect to device {0}".format(err))
                sys.exit(1)
            pems = ModuleTable(dev)
            pems.get()
            print(pems)
            chassis_power = dev.rpc.get_power_usage_information(normalize=True)
            tmp_pem_name = list()
            tmp_pem_serial = list()
            tmp_pem_state = list()
            for pem, i in zip(pems, chassis_power):
                tmp_pem_name[:] = []
                tmp_pem_serial[:] = []
                tmp_pem_state[:] = []
                p_name = i.findtext(".//name")
                print(pem.jname)
                if p_name == pem.jname:
                    p_state = i.findtext(".//state")
                    print(p_state)
                    tmp_pem_name.append(p_state)
                print(pem.sn)
                tmp_pem_name.append(pem.jname)
                tmp_pem_serial.append(pem.sn)
            pem_name.append(tmp_pem_name)
            pem_serial.append(tmp_pem_serial)
            pem_state.append(tmp_pem_state)

            dev.close()

        print(devices)
        print(pem_name)
        print(pem_state)
        print(pem_serial)
        df = pd.DataFrame({"devices":devices,
                           "pem name":pem_name,
                           "pem state":pem_state,
                           "pem serial":pem_serial})
        writer = ExcelWriter("inventory.xlsx")
        df.to_excel(writer, index=False)
        writer.save()

if __name__ == "__main__":
    print(get_info())