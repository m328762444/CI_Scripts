
### python 2.7 ###
## python-jenkins 1.1 version ##
import jenkins
import re
import sys
import os
import json
import subprocess
from collections import defaultdict
nodesdict={}
idlenodedict = defaultdict(list)
RunningJobs = []
Runningnodedict = {}
RunningDomains = []
JOB_Pre = sys.argv[1]
JENKINS_URL="http://myjenkins:8080"
JENKINS_USERNAME = "myname"
JENKINS_PASSWD = "mypasswd"
DomBuild = []
SpeciJobs=[JOB_Pre + 'Build',JOB_Pre + 'BnI']
PORT = 29418
HOST = "androidhub.mycompany.com"
p = subprocess.Popen('whoami', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = p.communicate()
USER = stdout.replace('\n','')

server=jenkins.Jenkins(JENKINS_URL,JENKINS_USERNAME,JENKINS_PASSWD)

def GetDomains():
        print "== Enter sub function GetDomains() now =="
        global DomBuild
        sshstring="ssh -p "+ str(PORT)+" "+ USER + "@" + HOST + " gerrit query --format=JSON branch:"+ os.environ['BRANCH'] + " --current-patch-set status:open label:Code-Review+2 label:Domain-Code-Review+1 NOT label:Code-Review-2 NOT label:Domain-Code-Review-1 NOT label:Verified-1 NOT label:Verified+1 is:mergeable | egrep 'project|^  number|revision|Depends-On:'"
        #print sshstring
        changes = []
        process = subprocess.Popen(sshstring, shell=True,stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        process.poll()
        while 1:
                context = process.stdout.readline()
                if not context:
                        break
                changes.append(json.loads(context))
        for change in changes:
                #print change[u'commitMessage']
                searchobj = re.search('Domain\s*?:.*?(\w+)\s*\\\\n',json.dumps(change[u'commitMessage']))
                if searchobj:
                        #print json.dumps(change[u'commitMessage'])
                        #print str(searchobj.groups(1)[0])
                        if searchobj.groups(1)[0] not in DomBuild:
                                DomBuild.append(searchobj.groups(1)[0])
        if len(DomBuild) > 0:
                print "Domain need to build in gerrit: "
                print DomBuild
        else:
                print "No changes need to be build Now"
                sys.exit(0)
        print "== Leave sub function GetDomains() now =="

def GetNodesInfo():
        print "== Enter sub function GetNodesInfo() now =="
        nodesinfo=server.get_nodes()
        for i in range(0, len(nodesinfo)):
                if not nodesinfo[i]['offline']:
                                if nodesinfo[i]['name'] != "master":
                                        numExecutors = server.get_node_info(nodesinfo[i]['name'])['numExecutors']
                                        nodesdict[nodesinfo[i]['name'].encode('utf-8')]=numExecutors
                                        #print nodesinfo[i]['name'] + "=====" + str(nodesdict[nodesinfo[i]['name']])
        print "nodesdict :"
        print nodesdict
        print "== Leave sub function GetNodesInfo() now =="

def GetRuningInfo():
        print "== Enter sub function GetRuningInfo() now =="
        RunningBuilds = server.get_running_builds()
        if len(RunningBuilds) < 1:
                print "No job is running now"
        else:
                for i in range(0, len(RunningBuilds)):
                        if RunningBuilds[i]['node'] not in Runningnodedict:
                                Runningnodedict[RunningBuilds[i]['node'].encode('utf-8')] = 1
                        else:
                                Runningnodedict[RunningBuilds[i]['node'].encode('utf-8')] += 1
                        if RunningBuilds[i]['name'] not in RunningJobs:
                                RunningJobs.append(RunningBuilds[i]['name'].encode('utf-8'))
                        #print Runningnodedict[RunningBuilds[i]['node']]
                # Get Runing Jobs's Parameter DOMAIN#
                #RunningJobs.remove(os.environ['JOB_NAME'])
                for specijob in SpeciJobs:
			if specijob in RunningJobs:
                        	RunningJobs.remove(specijob)
                for tmpjob in RunningJobs:
                        searchobj = re.search(JOB_Pre + "[a-zA-Z0-9]+$",tmpjob)
                        if searchobj:
                                build_num = server.get_job_info(tmpjob)['lastBuild']['number']
                                build_info = server.get_build_info(tmpjob,build_num)
                                #print build_info
                                print build_info['actions'][0]['parameters'][1]['value']
                                if build_info['actions'][0]['parameters'][1]['value'] not in RunningDomains:
                                                RunningDomains.append(build_info['actions'][0]['parameters'][1]['value'].encode('utf-8'))
                # Get Runing Jobs's Parameter DOMAIN#
        print "RunningDomains: "
        print RunningDomains
        print "RunningDomains number is : " + str(len(RunningDomains))
        print "RunningJobs: "
        print RunningJobs
        print "Runningnodedict: "
        print  Runningnodedict
        print "== Leave sub function GetRuningInfo() =="


def GetJobsInfo():
        print "== Enter sub function GetJobsInfo() now =="
        regexjobs = server.get_job_info_regex(JOB_Pre)
        for i in range(0, len(regexjobs)):
		if regexjobs[i]['name'] not in SpeciJobs:
                	searchobj1 = re.search("Update_Success", regexjobs[i]['name'])
                	searchobj2 = re.search("Trigger",regexjobs[i]['name'])
                	if not searchobj1 and not searchobj2:
                        	if regexjobs[i]['color'] != "disabled":
                                	if regexjobs[i]['name'] not in RunningJobs:
                                        	buildnum=server.get_job_info(regexjobs[i]['name'])['lastBuild']['number']
                                        	node=server.get_build_info(regexjobs[i]['name'],buildnum)['builtOn'].encode("utf-8")
                                        	idlenodedict[node].append(regexjobs[i]['name'].encode('utf-8'))
        print "idlenodedict: "
        print idlenodedict
        print "== Leave sub function GetJobsInfo() =="

def GetSingleIdleNode():
        print "== Enter sub function GetSingleIdleNode() now =="
        for node in idlenodedict:
                #print node + "==========="
                #print Runningnodedict
                if node not in Runningnodedict:
			print node
                        return node
        return None
        print "== Leave sub function GetSingleIdleNode() =="
def GetMinExcutorNode():
	print "== Enter sub function GetMinExcutorNode() now =="
        for node in idlenodedict:
                #print node + "==========="
                #print Runningnodedict
                if Runningnodedict[node] < nodesdict[node]:
			print node
                        return node
        return None
        print "== Leave sub function GetMinExcutorNode() =="

def TriggerBuild(jobname,domainname):
        print "== Enter sub function TriggerBuild() now =="
        #arg1=jobname,arg2=domainname #
        print jobname + " == " + domainname
        print domainname + " Domain build will be trigged."
        builddict = {'BRANCH':os.environ['BRANCH'],'DOMAIN':domainname,'CLEANBUILD':'0'}
        print builddict
        server.build_job(jobname, builddict)
        print jobname + " has been trigged for Domain " + domainname +"!"
        print "== Leave sub function TriggerBuild() =="

def Main():
        print "== Enter function Main() now =="
        GetDomains()
        GetNodesInfo()
        GetRuningInfo()
        GetJobsInfo()
        for domain in DomBuild:
                if domain in RunningDomains:
                        print domain  + "Domain Job is already runing now" + "\n"
                else:
			tmpnode1 = GetSingleIdleNode()
			if tmpnode1:
				idlenode = tmpnode1
			else:
				tmpnode2 = GetMinExcutorNode()
				if tmpnode2:
					idlenode = tmpnode2
				else:
					idlenode = None				    
                        print idlenode
                        if idlenode:
                                #print idlenodedict[idlenode]
                                TriggerBuild(idlenodedict[idlenode][0],domain)
                                idlenodedict[idlenode].remove(idlenodedict[idlenode][0])
                                #print idlenodedict[idlenode]
				if idlenode in Runningnodedict:
					Runningnodedict[idlenode] += 1
				else:
					Runningnodedict[idlenode] = 1
				if not idlenodedict[idlenote]:
					delete idlenodedict[idlenote]
                                #print Runningnodedict
                                RunningDomains.append(domain)
                                #print RunningDomains
                        else:
				print "All build server is runing now, Please waitting !"
                                
        print "== Leave function Main() now =="
Main()
