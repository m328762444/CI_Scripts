import os
import subprocess
import sys
import re
import xml.etree.ElementTree as ET
pathfile = "Android_Stash_ChangeList_1.txt"
sourcedir = os.getcwd()
GLRepos = {} #GL Repos path
precommitdict={} #project:prerevision
nowcommitdict={} #project:nowrevision

def GetGLReposPath():	
	print "Enter function GetGLReposPath()"
	MANIFEST_FILE = ".repo/manifest.xml"
        tree = ET.parse(MANIFEST_FILE)
        root = tree.getroot()
        for child in root.iter('project'):
		name = child.get('name')
                rp = child.get('revision')
                if rp == os.environ['BRANCH']:
                        pp = os.path.join(sourcedir,child.get('path'))
                        GLRepos[name] =	pp
        print "GLRepos as below:"
        print GLRepos
	print "Leave function GetGLReposPath()"

def GetRevision(arg1,aDict):
	print "Enter function GetRevision()"
	print "arg1 is " + arg1
	if os.path.isfile(arg1):
		print "arg1 is " + arg1
		tree = ET.parse(arg1)
        	root = tree.getroot()
        	for child in root.iter('project'):
                	name = child.get('name')
                	#path = child.get('path')
                	revision = child.get('revision')
                	if name in GLRepos:
                        	aDict[name] = revision
        #print "GLRepos as below: \n"
        #print GLRepos
	else:
		print "Error: arg1 is not exist, Please Check!"

	print "Leave function GetRevision()"

def Main():
	print "Enter function Main()"
	GetGLReposPath()
	GetRevision(os.environ['PreTag'],precommitdict)
	print "precommitdict as below:"
	print precommitdict
	GetRevision(os.environ['NowTag'],nowcommitdict)
	print "nowcommitdict as below:"
	print nowcommitdict

	for key in GLRepos:
		if key not in precommitdict:
			precommitdict[key] = 'addproject'
		if precommitdict[key] == nowcommitdict[key]:
			pass
		else:
			print "has different commitid, write to config file"
			with open(pathfile, "a") as f:
				f.write(key+"="+GLRepos[key]+"="+precommitdict[key]+"="+nowcommitdict[key]+"\n")
			f.close()
	print "Leave function Main()"
Main()
