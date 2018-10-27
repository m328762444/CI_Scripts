# CI_Scripts
Scripts Used for CI Build based on gerrit/bitbucket and other useful scripts

## submodule
### 1.submodule/GetSubmoduleInfo.py:
	GetSubmoduleInfo.py to get submodule information under submodule main repo 
	python GetSubmoduleInfo.py submodulecommit ==> output commitidfile.txt 
	print "python GetSubmoduleInfo.py submodulepath ==> output submodulepath.txt 
	print "python GetSubmoudleInfo.py submodulemanifest ==> output submodulemanifest.xml 
### 2.submodule/GetSubmoduleInfo.py:
	GetSubmoduleChangelist.pl to get changelist between two version.
	input===> version1_commitidfile.txt version2_commitidfile.txt 
	output==>changelist.html
### 3.useful submodule command:
```
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
```
## taginfo:
### 1.taginfo/setTag.py:
	For android project:python setTag.py branchname ABC_MY19_MAINLINE.json
## changelist:
	Get Changelists for project use repo manifest
### 1.changelist/Android_Stash_ChangeList_1.py:
	Android_Stash_ChangeList_1.py to generate a file contains the difference commitid between PreTag and NowTag on the BRANCH and their path.
	input===> 
	os.environ['BRANCH’] to get the projects in .repo/manifest.xml on BRANCH
	os.envirom['PreTag'] is the pretag manifestfile
	os.environ['NowTag'] is the NowTag manifestfile
	output===>
	Android_Stash_ChangeList_1.txt
### 2.changelist/Android_Stash_Changelist_2.pl:
	Android_Stash_Changelist_2.pl generate the changelist between two Tags.
	input===> Android_Stash_ChangeList_1.txt
	output===> Android_Stash_ChangeList_2.html
	for add projects will get the number of project merged changenumbers to get the project changelist.
## confluence:
	Update confluence page automatically with text, attachfile or html
### 1.confluence/BuildServer_Accout_Update.sh:
	BuildServer_Accout_Update.sh to get every build server username name and their infomation from /etc/passwd, generate a html table file==htmlbody.html.
### 2.confluence/confluence_page.py:
	input: htmlbody.html
	output: update the confluence page wih htmlbody.html
	you can also modify the python scripts to update your page with text or attach files to your page.
