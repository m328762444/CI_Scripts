#!/usr/bin/env python
from fabric.api import *
from fabric.context_managers import *
from fabric.contrib.console import confirm
env.usr='root'
env.gateway='192.168.1.23'
env.hosts=['192.168.1.21', '192.168.1.22']
env.passwords = {
	'root@192.168.1.21:22':'LKs934jh3',
	'root@192.168.1.22:22':'LKs934jh3',
	'root@192.168.1.23:22':'UI7384hg6'
}
lpackpath="/home/install/lnmp0.9.tar.gz"
rpackpath="/tmp/install/"
@task
def put_task():
	run ("mkdir -p /tmp/install")
	with setting(warn_only=True):
		result = put(lpackpath, rpackpath)
		if result.failed and not confirm("put file failed, Continue[Y/N]?"):
			abort("Aborting file put task!")
@task
def run_task():
	with cd("/tmp/install"):
		run("tar -zxvf lnmp0.9.tar.gz")
		with cd("lnmp0.9/"):
			run (".'centos.sh")
@task
def go():
	put_task()
	run_task()
