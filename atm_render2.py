from jinja2 import Environment, FileSystemLoader
import pandas
import yaml
from pprint import pprint
import ipaddress

file = FileSystemLoader(".")
env = Environment(loader=file)
template = env.get_template("template.j2")

filename = "ATM-3G.xlsx"

hostname = pandas.read_excel(filename, usecols="B", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
kcell = pandas.read_excel(filename, usecols="C", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
tele2 = pandas.read_excel(filename, usecols="G", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
kcell_ip = pandas.read_excel(filename, usecols="D", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
tele2_ip = pandas.read_excel(filename, usecols="H", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
int_ip = pandas.read_excel(filename, usecols="J", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()
tunn_ip = pandas.read_excel(filename, usecols="I", skiprows=1000, sheet_name="ATMs", header=None).values.tostring()

df_username = pandas.read_excel("PPP-User.xlsx", usecols="B", skiprows=1, sheet_name="Лист1", header=None).values.tolist()
df_values = pandas.read_excel("PPP-User.xlsx", usecols="E", skiprows=1, sheet_name="Лист1", header=None).values.tolist()

for j in range(len(hostname)):
    for i in range(len(df_username)):
        if df_username[i] == kcell[j]:
            with open("config/" + str(hostname[j]).strip("['']") + ".txt", "a") as f:
                ip_net = ipaddress.ip_address(str(int_ip[j]).strip("['']")) - 1

                rnd_tmp = template.render(apn_name=str(kcell[j]).strip("['']"),
                                          hostname=str(hostname[j]).strip("['']"),
                                          tunn_ip=str(tunn_ip[j]).strip("['']"),
                                          int_ip=str(int_ip[j]).strip("['']"),
                                          router_id=str(tunn_ip[j]).strip("['']"),
                                          p2p_net=ip_net,
                                          apn_pass=str(df_values[i]).strip("['']"))
                f.write(rnd_tmp)
        else:
            continue