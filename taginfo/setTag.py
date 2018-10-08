# Creating daily Tag and commit
# For android project:python setTag.py $branch ABC_MY19_MAINLINE.json

import json
import os
import sys
import filecmp
#import pdb

from tag import Tag

#pdb.set_trace()
sys.dont_write_bytecode = True

def initialize(tag_info_file):
    if os.path.exists(tag_info_file):
        tag = Tag(tag_info_file)
    else:
        print "Tag file doesn't exists!!!"
    val = generateTaggedXml()
    if val:
        currentTag = tag.get_current_tag()
        os.chdir("../")
        tag.update_tag_info_file()
        commitChange(currentTag)
        tagCommit(currentTag)
        pushtag(currentTag)
        os.chdir(sys.path[0])
        updateGerrit()

def generateTaggedXml():
    os.chdir("../../../")
    os.system("pwd")
    os.system("rm -f " +sys.argv[1] + "_tagged.xml")
    os.system("repo manifest -o " +sys.argv[1] + "_tagged.xml -r")
    if os.path.exists(sys.argv[1] + "_tagged.xml"):
        print "Tagged file generated"
        if not (filecmp.cmp( sys.argv[1]+ '_tagged.xml', '.repo/manifests/' +sys.argv[1] + '_tagged.xml')):
            print "New changes Exists!!!"
            os.system("mv " +sys.argv[1] + "_tagged.xml .repo/manifests/")
            os.chdir(sys.path[0])
#            os.chdir(sys.path[0] + ".repo/manifests/")
            return 1
        else:
            print "No new changes. Exit !!!"
            return 0
    else:
        os.chdir(sys.path[0])
        print "Tagged file not generated. Exit !!!"
        return 0

def commitChange(currentTag):
    print "\nCurrent Tag = " + currentTag
    os.system("git add ../" +sys.argv[1] + "_tagged.xml")
    os.system("git add " + sys.argv[2])
    commitMessage = "Summary : Daily Build Tag "
    commitMessage +=  currentTag
    commitMessage +=  "\n\nDescription :  Daily Build Tag "
    commitMessage +=  currentTag
    commitMessage +=  "\nChange-Type : Integration\nDomain : BnI\nTracking-Id : NA\nDepends-On : 00\nUnit-Test : NA\n"
    commitCommand = "git commit -m \'" + str(commitMessage) + "\'"
    os.system(commitCommand)
    print "Commit Message::\n" + commitCommand
    pushCommit()

def pushCommit():
#To push change for review
#    os.system("git push origin HEAD:refs/for/"  +sys.argv[1] + "/BnI")
    print "Pushing Commit on branch " + sys.argv[1]
    os.system("git push origin HEAD:refs/heads/"  +sys.argv[1])

def tagCommit(currentTag):
    print "Tagging commit; TAG: " + currentTag
    os.system("git tag -a " + currentTag + " -m \"Daily build tag " + currentTag + "\"")

def pushtag(currentTag):
    print "Pushing TAG: " + currentTag
    os.system("git push origin " + currentTag)

initialize(sys.argv[2])
