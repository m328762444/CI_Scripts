#!/usr/bin/python
import paramiko
hostname = '10.80.105.191'
username = 'gama'
password = 'sw_integration'
paramiko.util.log_to_file('syslogin.log')
ssh = paramiko.client.SSHClient()
ssh.load_system_host_keys()
ssh.connect(hostname=hostname, username=username, password=password)
stdin, stdout, stderr = ssh.exec_command('free -m')
print stdout.read()
stdout.readlines()
ssh.close()
