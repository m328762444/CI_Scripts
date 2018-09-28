# CI_Scripts
Scripts Used for CI Build based on gerrit/bitbucket and other useful scripts

submodule
1.submodule/GetSubmoduleInfo.py:
	GetSubmoduleInfo.py to get submodule information under submodule main repo
	python GetSubmoduleInfo.py submodulecommit ==> output commitidfile.txt
	print "python GetSubmoduleInfo.py submodulepath ==> output submodulepath.txt
	print "python GetSubmoudleInfo.py submodulemanifest ==> output submodulemanifest.xml
2.submodule/GetSubmoduleInfo.py:
	GetSubmoduleChangelist.pl to get changelist between two version.
	input===>version1_commitidfile.txt  version2_commitidfile.txt 
	output==>changelist.html
