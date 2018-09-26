#!/usr/bin/python
# This script used to get submodule commit id
# Please put it to the source root dir to run
# output : commitidfile.txt
import os
import sys
import subprocess
sourcedir = os.getcwd()
modulefile = '.gitmodules'
#commitfile = os.getcwd() + "/commitidfile.txt"
submodules = {} #url-->{path,branch}
def getmoduledata(filetmp):
	print "############## getmoduledate() ##################"
        with open(filetmp) as f:
		pathtmp = ""
		pathpre = os.path.split(filetmp)[0]
                for line in f.readlines():
                        line = line.rstrip('\n')
			#print line
			if 'path' in line:
				pathtmp = pathpre + "/" + line.split()[2]
				submodules[pathtmp] = { 'url' : None, 'branch' : 'master' }
			elif 'url' in line:
				#print pathtmp + "== url: " + line.split()[2]
				submodules[pathtmp]['url'] = line.split()[2]
			elif 'branch' in line:
				#print pathtmp + "== branch: " + line.split()[2]
				submodules[pathtmp]['branch'] = line.split()[2]
	print "###################################################"


def getcommitid():
	print "################## getcommitid() #################"
	for key in submodules.keys():
		#print key
		#print "========" + submodules[key]['url']
		#print "========" + submodules[key]['branch']
        	os.chdir(key)
		gitcmd = "git rev-parse HEAD"
		p = subprocess.Popen(gitcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout,stderr=p.communicate()
		commitid = stdout.replace('\n','')
		submodules[key]['commitid'] = commitid
		#print "========" + submodules[key]['commitid']
	print "###################################################"

def parsemodulefile():
	print  "############## parsemodulefile() ##################"
	for foldername, subfolders, filenames in os.walk(sourcedir):
        	foldernamepath = foldername
        	for filename in filenames:
                	filepath = os.path.join(foldernamepath, filename)
                	if modulefile in filepath:
                     		#print ("====" + filepath)
                     		getmoduledata(filepath)
	print "###################################################"

def getmainrepoinfo():
	print  "############## getmainrepoinfo() ##################"
	pathtmp = os.getcwd()
	submodules[pathtmp] = { 'url' : None, 'branch' : 'master' }
	giturlcmd = "git remote -v|grep fetch|gawk '{print $2}'"
	p = subprocess.Popen(giturlcmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	stdout, stderr=p.communicate(0)
	url = stdout.replace('\n','')
	submodules[pathtmp]['url'] = url
	#submodules[pathtmp]['branch'] = master
	print "###################################################"
def genmanifest():
	print "############## genmanifest() ##################"
	manifestfile = sourcedir + "/submodulemanifest.xml"
	print "## output file is " + manifestfile +" #####"
	manifesthead = '<?xml version="1.0" encoding="UTF-8"?>' + "\n" + '<manifest>' + "\n" + "<notice>CLUSTER_Ring='0'</notice>" + "\n" + '<remote name="origin" fetch="ssh://git@stash1.harman.com:7999/"/>' + "\n" + '<default remote="origin"/>' + '\n'
	manifesttail = '</manifest>' 
	#print manifesthead
	sshsite='ssh://git@stash1.harman.com:7999/'
	if os.path.isfile(manifestfile):
                os.remove(manifestfile)
        for key in submodules.keys():
                with open(manifestfile, "a") as f:
			project = submodules[key]['url'].replace(sshsite,'')
			path = key.replace(os.path.dirname(sourcedir)+'/','')
			#print key + "===" + path
			f.write('  <project name=\"' + project + "\" path=\"" + path +"\" revision=\"" + submodules[key]['commitid'] + "\"/>\n")
		f.close()
	with open(manifestfile, 'r+') as f:
		content = f.read()
		f.seek(0,0)
		f.write(manifesthead + content)
	f.close()
	with open(manifestfile,"a") as f:
		f.write(manifesttail)
	f.close()
	print "###################################################"
def usage():
	print "###################### Usage #######################"
	print "GetSubmoduleInfo.py to get submodule information under submodule main repo\n"
	print "python GetSubmoduleInfo.py submodulecommit ==> output commitidfile.txt\n"
	print "python GetSubmoduleInfo.py submodulepath ==> output submodulepath.txt\n"
	print "python GetSubmoudleInfo.py submodulemanifest ==> output submodulemanifest.xml\n"
	print "###################################################"

def Main():
	print "###################### Main() #######################"
	getmainrepoinfo()
	parsemodulefile()
	if sys.argv[1] == "submodulecommit":
		getcommitid()
		commitfile = sourcedir + "/commitidfile.txt"
		print "## output file is " + commitfile +" #####" 
		if os.path.isfile(commitfile):
                	os.remove(commitfile)
        	for key in submodules.keys():
                	with open(commitfile, "a") as f:
                        	f.write(submodules[key]['url'] + "  :  " + submodules[key]['commitid'] + "\n")
        		f.close()
	elif sys.argv[1] == "submodulepath":
		pathfile = sourcedir + "/submodulepath.txt"
		print "## output file is " + pathfile +" #####"
		if os.path.isfile(pathfile):
			os.remove(pathfile)
		for key in submodules.keys():
                	with open(pathfile, "a") as f:
                        	f.write(key + " : " + submodules[key]['url'] + "\n")
        		f.close()
	elif sys.argv[1] == "submodulemanifest":
		getcommitid()
		genmanifest()
	else:
		print "ERROR!!!! Please check your parameters !!!!!!!!!!!!!!"
		usage()
	print "###################################################"
Main()
