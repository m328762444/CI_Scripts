#!/usr/bin/env python
from fabric.api import *
env.user='gama'
env.hosts=['10.80.105.177','10.80.105.179']
env.passwd='sw_integration'
@runs_once #check local system info, run once when have more hosts
def local_task():
	local("uname -a")
def remote_task():
	with cd ("/var/log"):
		run ("ls -l")

