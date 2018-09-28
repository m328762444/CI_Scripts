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
3.useful submodule command:
	pushd /path/to/mainrepo
	echo "git checkout master";
	git checkout master >/dev/null
	echo "git clean -xdf"
	git clean -xdf >/dev/null
	echo "git pull origin master";
	git pull origin master >/dev/null
	echo "git reset --hard origin/master"
	git reset --hard origin/master >/dev/null
	echo "git submodule update --init --recursive"
	git submodule update --init --recursive > /dev/null
	echo "git submodule foreach --recursive git checkout master"
	git submodule foreach --recursive git checkout master > /dev/null
	echo "git submodule foreach --recursive git clean -xdf";
	git submodule foreach --recursive git clean -xdf > /dev/null
	echo "git submodule foreach --recursive git pull origin master"
	git submodule foreach --recursive git pull origin master >/dev/null
	echo "git submodule foreach --recursive git reset --hard origin/master"
	git submodule foreach --recursive git reset --hard origin/master > /dev/null

