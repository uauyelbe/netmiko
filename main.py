import netmiko
from netmiko import ConnectHandler
import xml.etree.ElementTree as et
import string
from getpass import getpass
from netmiko import ConnectHandler, cisco, NetMikoAuthenticationException

psw = getpass()

tmstmp_dbg = "service timestamps debug datetime msec localtime year"
tmstmp_log = "service timestamps log datetime msec localtime year"
syslog_cmnd = [ "logging 192.168.1.1", "logging 192.168.20.20", "logging 10.246.255.2" ]
buffer_cmnd = [ "logging buffered 1024000 debugging", "no logging console" ]
time = [ "clock timezone ALA 6 0" ]
ntp_cmnd = [ "ntp server 10.246.1.140", "ntp server 192.168.80.80" ]

admin = "username admin privilege 15 secret RestictedAccess"
admin2 = "username admin2 privilege 15 secret NotAllowed"
 
config_commands = [ tmstmp_dbg, tmstmp_log ]

from xml.dom import minidom
xmldoc = minidom.parse('data.xml')
itemlist = xmldoc.getElementsByTagName('sysname')
print(len(itemlist))


def syslog(cmnd_syslog, ipaddr):
	syslog_list = [
	'192.168.1.1',
	'10.246.255.2',
	'192.168.20.20'
	]
	
	for ip in syslog_list:
		if ip not in cmnd_syslog:
			print("syslog list is not full " + ip + " " + ipaddr)
			syslog_config = ssh_connection.send_config_set(syslog_cmnd)
			res.write("syslog is corrected\n")
		else:
			print("syslog ip " + ip + " exists")
			res.write("syslog is ok " + ip + "\n")
			
def tmstmp(cmnd_tmstmp, ipaddr):
	if tmstmp_dbg or tmstmp_log not in cmnd_tmstmp:
		print("correcting timestamp debug and log")
		res.write("timestamp debug " + ipaddr + "\n")
		try:
			result = ssh_connection.find_prompt() + "\n"
			result = ssh_connection.send_config_set(config_commands)
			res.write("timestamp is corrected\n")
		except:
			print(ipaddr + " unable to enter configuration mode")
		
	else:
		print("timestamp debug is ok")
		
def logbuffer(ipaddr):
	try:
		buffer = ssh_connection.find_prompt() + "\n"
		buffer = ssh_connection.send_config_set(buffer_cmnd)
	except:
		print(ipaddr + " unable to enter configuration mode")
		
def timezone(ipaddr, cmnd_time):
	if "ALA" not in cmnd_time:
		try:
			result_t = ssh_connection.find_promt() + "\n"
			result_t = ssh_connection.send_config_set(time)
		except:
			print(ipaddr + " unable to enter configuration mode")
	else:
		print("time is ok")
		res.write(cmnd_time + "\n")
		
ntp1 = "10.246.1.140"
ntp2 = "192.168.80.80"
def ntp(ipaddr, cmnd_ntp):
	if ntp1 or ntp2 not in cmnd_ntp:
		print("ntp is not ok")
		result_ntp = ssh_connection.send_config_set(ntp_cmnd)
		res.write("====ntp====\n")
		res.write("ntp is corrected\n")
	else:
		print("ntp is ok")
		res.write("====ntp====\n")
		res.write("ntp is ok\n")
		
def local_user(ipaddr, cmnd_user):
	if "admin" not in cmnd_user:
		print("user admin doesn't exist")
		result_user = ssh_connection.send_config_set(admin)
		res.write("user admin is added\n")
	else:
		print("user admin is ok")
		res.write("user admin is ok\n")
		
	if "admin2" not in cmnd_user:
		print("user admin2 doesn't exist")
		result_user = ssh_connection.send_config_set(admin2)
		res.write("user admin2 is added\n")
	else:
		print("user admin2 is ok")
		res.write("user admin2 is ok\n")
		
def logging(ipaddr, cmnd_sync):
	c = cmnd_sync.count("synchronous")
	if c < 3:
		print("synchronous not enought")
		res.write("add synchronous " + ipaddr + "\n")
	else:
		print("synchronous is ok")
		res.write("synchronous is ok\n")

tacacs_odt = "10.245.113.34"
tacacs_gcust = "10.246.255.50"
def tacacs(ipaddr, cmnd_tacacs):
	if tacacs_odt not in cmnd_tacacs:
		print("main tatacs does not exist")
		res.write("add main tacacs " + ipaddr + "\n")
	else:
		print("main tatacs is ok")
		res.write("main tatcs is ok\n")
		
	if tacacs_gcust not in cmnd_tacacs:
		print("tacacs gcust does not exist")
		res.write("add tatacs gcust " + ipaddr + "\n")
	else:
		print("tacacs gcust is ok")
		res.write("tacacs gcust is ok")

for s in itemlist:
	ipaddr = s.attributes['ip'].value
	#sysname = s.attributes['sysname'].value
	try:
		ssh_connection = ConnectHandler(
			device_type='cisco_ios',
			ip=ipaddr,
			username="root",
			password=psw,
			port=22
		)
	except:
		try:
			ssh_connection = ConnectHandler(
				device_type='cisco_ios_telnet',
				ip=ipaddr,
				username="root",
				password=psw,
				port=23
			)
		except:
			print("Unable to connect " + ipaddr)
			continue
						
	with open("result.txt", "a") as res:
		#cmnd_syslog = ssh_connection.send_command("sh run | in logging")
		#cmnd_tmstmp = ssh_connection.send_command("sh run | in timestamp")
		#cmnd_time = ssh_connection.send_command("sh clock")
		cmnd_ntp = ssh_connection.send_command("sh run | in ntp")
		cmnd_user = ssh_connection.send_command("sh run | in admin")
		cmnd_sync = ssh_connection.send_command("sh run | b line")
		cmnd_tacacs = ssh_connection.send_command("sh run | in server-priv")
		
		res.write(ipaddr + "\n")
		
		print("checking syslog")
		syslog(cmnd_syslog, ipaddr)
		
		print("checking timestamp")
		tmstmp(cmnd_tmstmp, ipaddr)
		
		print("loggin buffer")
		logbuffer(ipaddr)
		res.write("buffer size increased " + ipaddr + "\n")
		
		print("timezone")
		timezone(ipaddr, cmnd_time)
		res.write("timezone checked\n")
		
		print("ntp")
		ntp(ipaddr, cmnd_ntp)
		res.write("ntp checked\n")
		
		print("local user")
		local_user(ipaddr, cmnd_user)
		res.write("local user checked\n")
		
		print("synchronous")
		logging(ipaddr, cmnd_sync)
		res.write("synchronous is checked\n")
		
		print("tacacs")
		tacacs(ipaddr, cmnd_tacacs)
		res.write("tacacs checked\n")
		
		sequ = ssh_connection.send_config_set("service sequence-numbers")
		
		wr = ssh_connection.send_command("wr")
		
		res.write("==============================\n")
		ssh_connection.disconnect()
		print(ipaddr+" done")
		print("=============================\n")