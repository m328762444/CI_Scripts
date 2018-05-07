#!/usr/bin/env python
from fabric.api import *
env.user='gama'
env.hosts=['10.80.105.177','10.80.105.179']
env.password='sw_integration'
@runs_once #walkround hosts, only the first host run
def input_raw():
	return prompt("please input directory name: ", default="/home")
def worktask(dirname):
	run ("ls -l "+dirname)
@task #only go function display to fab
def go():
	getdirname = input_raw()
	worktask(getdirname)
