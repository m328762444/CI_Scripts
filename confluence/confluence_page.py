# Update Confluence Page
# author:  GaMa
# email:   ganglong.ma@harman.com
# date:    2018-10-08

import json
import requests
import os
baseurl = "https://confluence.mycompany.com/confluence/rest/api/content/"
username = "myname"
password = "mypasswd"
os.environ['HTTP_PROXY'] = 'http://xx.xx.xx.xx:xxxx'
os.environ['HTTPS_PROXY'] = 'https://xx.xx.xx.xx:xxxx'
proxyDict = {
	"http":os.environ['HTTP_PROXY'],
	"https":os.environ['HTTPS_PROXY']
       }
def get_page_json(page_id, expand = False):
	print "========= Enter SubFunciton get_page_json() ========="
	if expand:
		suffix = "?expand=" + expand  #body.storage
	else:
		suffix = ""

	url = baseurl + page_id + suffix
	response = requests.get(url, auth=(username,password),proxies=proxyDict)
	response.encoding = "utf8"
	return json.loads(response.text)
	print "========= Leave SubFunciton get_page_json() ========="
#print (get_page_json("156967685","body.storage"))
#json_data=get_page_json("156967685","body.storage")
#print (json_data['title'])
#print (json_data['body']['storage']['value'])

def set_page_json(page_id, json_content):
	print "========= Enter SubFunciton set_page_json() ========="
	headers = {
		'Content-Type':'application/json',
	}
	
	response = requests.put(baseurl + page_id, headers = headers, data=json.dumps(json_content),auth=(username,password),proxies=proxyDict)
	return(response.text)
	print "========= Leave SubFunciton set_page_json() ========="

def attach_file_to_page(page_id, filepath, filename):
	print "========= Enter SubFunciton attach_file_to_page() ========="
	headers = {
		'X-Atlassian-Token': 'no-check',
	}
	
	files = {
		'file':(filename, open(filepath, 'rb')),
	}

	#delete attach with the same name
	response = requests.get(baseurl + page_id + "/child/attachment", auth=(username, password),proxies=proxyDict)
	for attachment in json.loads(response.text)['results']:
		if attachment['title'] == filename:
			requests.delete(baseurl + attachment['id'], headers=headers, auth=(username, password),proxies=proxyDict)
	#attach files
	response = requests.post(baseurl + page_id + "/child/attachment", headers=headers, files=files,auth=(username, password),proxies=proxyDict)
	return(response.text)
	print "========= Leave SubFunciton attach_file_to_page() ========="

def read_file_as_str(file_path):
	print "========= Enter SubFunciton read_file_as_str() ========="
	if not os.path.isfile(file_path):
		raise TypeError(file_path + "does not exist")
	all_the_text = open(file_path).read()
	return all_the_text
	print "========= Leave SubFunciton read_file_as_str() ========="
def Main():
	print "========= Enter SubFunciton Main() ========="
	#print (get_page_json("156967685","body.storage"))
	print ("############################################")
	print (get_page_json("156967685"))
	json_data = get_page_json("156967685")
	new_json_data = dict()
	new_json_data['id'] = json_data['id']
	new_json_data['type'] = json_data['type']
	new_json_data['title'] = json_data['title']
	new_json_data['version'] = {"number":json_data['version']['number'] + 1}
	if not 'key' in json_data:
		new_json_data['key'] = json_data['space']['key']
	else:
		new_json_data['key'] = json_data['key']
	
	## normal update confluence page ##
	#new_json_data['body'] = {'storage':{'value':'<p>This is the updated text for the new page</p>','representation':'storage'}}
	## update with attachment ##
	#attach_file_to_page("156967685","data/test.jpg","test.jpg")
	#img_url = "https://confluence.harman.com/confluence/download/attachments/156967685/test.jpg"
	#new_json_data['body'] = {'storage':{'value':'<img src="'+img_url+'"></img>','representation':'storage'}}
	
	# upHTMKdate with html table #
	htmlcontent = json.dumps(read_file_as_str("htmlbody.html"))
	new_json_data['body'] = {'storage':{'value':'<p>'+ htmlcontent +'</p>','representation':'storage'}}
	print ("##################################")
	print new_json_data
	print ("##################################")
	print (set_page_json("156967685",new_json_data))
	print "========= Leave SubFunciton Main() ========="
Main()
