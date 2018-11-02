from os import listdir
from os.path import isfile, join
import pandas


# read data from excel format
def data_excel(filename, folder):
    # stores ip address and hostname in dict format
    data = dict()
    df = pandas.read_excel(folder + "/" + filename)
    ip_list = df["ip"].values
    host_list = df["hostname"].values
    for ip, host in zip(ip_list, host_list):
        data[ip] = host
    return data


# read data from txt format
def data_txt(filename, folder):
    # stores hostnames in list format
    data = list()
    mypath = folder + "/" + filename
    with open(mypath, "r") as bngmx:
        print("opening file " + f)
        bngmx = bngmx.readlines()
        for i in bngmx:
            data.append(str(i).strip())
    return data


# read from excel
def device_part(filename, folder):
    df = pandas.read_excel(folder + "/" + filename, usecols="B", skiprows=3, sheet_name="ЗИП Juniper Алматы", header=None)
    return df


if __name__ == "__main__":
    # directory where files are stored
    folder = "devices"
    # take the file's name from the directory
    filename = [f for f in listdir(folder) if isfile(join(folder, f))]
    for f in filename:
        if f.endswith(".txt"):
            print(data_txt(f, folder))
        elif f.endswith(".xlsx"):
            print(data_excel(f, folder))
    z = "ЗИП_ГЦУСТ_на_июль_2018г._v2.xls"
    print(device_part(z, folder))