# python 2.7 #
# python-jenkins 1.1.0 #
import os
import sys
if os.path.exists(os.path.join(os.getcwd(),"../python_packages")):
        sys.path.append(os.path.join(os.getcwd(),"../python_packages"))
        print "[info]: "+os.path.join(os.getcwd(),"../python_packages") + " exits!"
        print "[info]: will use python packages in local path!"
else:
        print "[info]: will use python packages in system path!"
import jenkins
import re
from datetime import datetime

AllNodes = ['10.80.105.181','10.80.105.182','10.80.105.183','10.80.105.191','10.80.105.192']
JENKINSURL = 'http://10.80.105.178:8080'
JENKINSUSER = 'jenkins'
JENKINSPASSWD = 'jenkins'
server = jenkins.Jenkins(JENKINSURL,JENKINSUSER,JENKINSPASSWD)
print os.environ['BRANCH']
def ReConfigNodes1():
	# check node's numberexecutor if not 1, reconfig to 1 #
	for node in AllNodes:
		if server.get_node_info(node)['numExecutors'] > 1:
			print "Node: " + node + " need to change numExecutors to 1"
			nodeconfig = server.get_node_config(node)
			newnodeconfig = re.sub("<numExecutors>"+str(server.get_node_info(node)['numExecutors'])+"</numExecutors>","<numExecutors>1</numExecutors>",nodeconfig)
			server.reconfig_node(node,newnodeconfig)
			print "Node: " + node + " numberExecutors has been changed to " + str(server.get_node_info(node)['numExecutors'])
		else:
			print "Node: " + node + " do not need to change numExecutors" 
def ReConfigNodes3():
	# check node's numberexecutor if not 3, reconfig to 3 #
	for node in AllNodes:
                if server.get_node_info(node)['numExecutors'] < 2:
                        print "Node: " + node + " need to change numExecutors to 3"
                        nodeconfig = server.get_node_config(node)
			newnodeconfig = re.sub("<numExecutors>"+str(server.get_node_info(node)['numExecutors'])+"</numExecutors>","<numExecutors>3</numExecutors>",nodeconfig)
                        server.reconfig_node(node,newnodeconfig)
                        print "Node: " + node + " numberExecutors has been changed to " + str(server.get_node_info(node)['numExecutors'])
                else:
                        print "Node: " + node + " do not need to change numExecutors"
def ReConfigNodes(number):
	# check node's numberexecutor if not 1, reconfig to 1 #
	# check node's numberexecutor if not 3, reconfig to 3 #
	for node in AllNodes:
                if server.get_node_info(node)['numExecutors'] !=  number:
                        print "Node: " + node + " need to change numExecutors to " + str(number)
                        nodeconfig = server.get_node_config(node)
                        newnodeconfig = re.sub("<numExecutors>"+str(server.get_node_info(node)['numExecutors'])+"</numExecutors>","<numExecutors>" + str(number) + "</numExecutors>",nodeconfig)
                        server.reconfig_node(node,newnodeconfig)
                        print "Node: " + node + " numberExecutors has been changed to " + str(server.get_node_info(node)['numExecutors'])
                else:
                        print "Node: " + node + " do not need to change numExecutors"
                    
def TriggerAllBuild():
	print "Starting Main Run " + '\n'
	if os.environ['BRANCH'] == 'n60-my20-mainline':
		JOB_Pre = "BJEVN60_Android_CI_"
	elif os.environ['BRANCH'] == 'gwm-my19-mainline':
		JOB_Pre = "GWM_V2MH_Android_CI_"
	else:
		print "Please contact integrator for help"
		sys.exit(0)
	alljobs = server.get_all_jobs()
	needbuildjobs = []
	for i in range(0, len(alljobs)):
		if alljobs[i]['color'] != 'disabled':
			searchobj = re.search(JOB_Pre + "[a-zA-Z0-9]+$", alljobs[i]['name'])
			if searchobj:
				needbuildjobs.append(alljobs[i]['name'])
   	'''
	if 'GWM_V2MH_Android_CI_BnI' in needbuildjobs:
		needbuildjobs.remove('GWM_V2MH_Android_CI_BnI')
	if 'GWM_V2MH_Android_CI_Migration' in needbuildjobs:
		needbuildjobs.remove('GWM_V2MH_Android_CI_Migration')
	if 'GWM_V2MH_Android_CI_Build' in needbuildjobs:
		needbuildjobs.remove('GWM_V2MH_Android_CI_Build')
	'''
	SpeciJobs = [JOB_Pre + 'Build', JOB_Pre + 'BnI']
       	for index, item in enumerate(SpeciJobs):
		print str(index) + "==" + item
		if item in needbuildjobs:
			needbuildjobs.remove(item)
	for i in range(0, len(needbuildjobs)):
		Dtopic = 'CLEANBUILD'
		print "Domain: " + Dtopic + " Job will be trigged" + "\n"
		builddict = {'BRANCH':os.environ['BRANCH'],'DOMAIN':Dtopic,'CLEANBUILD':"1"}
		print builddict
		server.build_job(needbuildjobs[i], builddict)
		print needbuildjobs[i] + " has been trigged!"
def Main_Run():
	today = datetime.now().date().isocalendar()[2]
	hour = datetime.now().hour
	if today >= 6:
		## change all nodes numberexecutor to 1 when satday ##
		#ReConfigNodes1()
		ReConfigNodes(1)
		## Trigger every domainbuild on the nodes ##
		TriggerAllBuild()
	elif today == 1 and hour < 12:
		## change all node numberexecutor to 3 when monday ##
		#ReConfigNodes3()
		ReConfigNodes(3)
	else:
		print "Now is " + str(today) + ":" + str(hour) + "(day:hour), don't need to do clean build" 
 
Main_Run()
