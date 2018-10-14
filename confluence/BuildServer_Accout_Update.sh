#!/bin/bash
echo "################################################"
echo "####### Get Every Linux Server account now #####"
sshuser="myname"
accountfile="$WORKSPACE/accounts.txt"
htmlfile="$WORKSPACE/htmlbody.html"
rm $accountfile
buildservers=('10.80.105.178' '10.80.104.120' '10.80.105.177' '10.80.105.179' '10.80.105.181' '10.80.105.182' '10.80.105.183' '10.80.105.191' '10.80.105.192')
htmlheader='<table><tr><th>Server IP</th><th>UserName</th><th>UserEmail</th></tr>'
htmltail='</table>'
htmlbodyhead='<tr><td></td><td>'
htmlbodymid='</td><td>'
htmlbodytail='</td></tr>'
echo $htmlheader > $htmlfile
for value in ${buildservers[@]}
do
  echo "==========$value============"
  htmlbody="<tr><td>"${value}"</td><td></td><td></td></tr>"
  #echo "$value" > $accountfile
  #echo "ssh $sshuser@$value \"cat /etc/passwd|awk -F: '{if ($3 >1001){print $1,$5}}';exit\""
  #ssh $sshuser@$value "cat /etc/passwd|awk -F: '{if (\$3 >1001){print \$1   \"==\"   \$5}}';exit"
  if [ "$value"x == "10.80.105.178"x ];then
  	account=$(cat /etc/passwd|awk -F: '{if ($3 >1001){print $1   "="   $5}}')
  else
  	account=$(ssh $sshuser@$value "cat /etc/passwd|awk -F: '{if (\$3 >1001){print \$1   \"=\"   \$5 "\n"}}';exit")
  fi
  echo "$account" > $accountfile
  sed -i '/'nobody'.*/d' $accountfile
  while read line
  do
	#echo $line
    username=`echo ${line%=*}`
    useremail=`echo ${line#*=}`
    echo "$username===========$useremail"
    htmlbody=${htmlbody}${htmlbodyhead}${username}${htmlbodymid}${useremail}${htmlbodytail}
  done< $accountfile
  echo "$htmlbody" >> $htmlfile
  echo "###############"
done 

echo $htmltail >> $htmlfile
cat $htmlfile

echo "############################################################"
echo "### Update Every Linux Server account to Conflunece Page ###"
cat htmlbody.html|tr -d '\n' >> tmp_htmlbody.html
mv tmp_htmlbody.html htmlbody.html
python confluence_page.py
popd

