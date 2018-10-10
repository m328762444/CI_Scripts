#!/usr/bin/perl
use strict;
use warnings;
use Cwd;
use Data::Dumper;
use File::Basename;
my $sourcedir=getcwd;
my $configfile = $sourcedir."/Android_Stash_ChangeList_1.txt";
print "$configfile\n";
my $changelog = $sourcedir."/Android_Stash_ChangeList_2.html";
print "$changelog\n";
my $changeurl;
my $username="myusername";
my $gerritserver="mygerritserver";
print $#ARGV;
print "###################";
if ($#ARGV+1 != 0){
   $changeurl=0;
   print "Don't need to get changeurl.\n";
}else{
   $changeurl=1;
   print "Will add changeurl to changelist.\n";
}

sub GetChangeList(){
       my $htmlhead = '<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}caption {text-align: left;}td {border: 1px solid black;text-align: left;padding: 8px;}th {border: 1px solid black;text-align: center;padding: 8px;}.row1 {background-color: #0088FF}.row2 {background-color: #DDDD00}.row3 {background-color: #DDDDDD}.row4 { background-color: #FFFFFF }</style></head><body><h2>Change List</h2><table>';
        if ($changeurl){
		$htmlhead=$htmlhead.'<tr class="row1"><th>ChangeNumber</th><th>Commit ID</th><th>Owner</th><th>CommitMessage</th></tr>';
        }else{
		$htmlhead=$htmlhead.'<tr class="row1"><th>Commit ID</th><th>Owner</th><th>CommitMessage</th></tr>';        }
	my $htmltail = '</body></html>';
        my $htmlbody = "";
        open(CONF,$configfile) or die "Can't open $configfile : $!";
        while(<CONF>){
            chomp($_);
            next if($_ eq '');
            if($_ =~ /(.+)=(.+)=(.+)=(.+)/){
                  my  $key1=$1;$key1 =~ s/^\s+//; $key1=~ s/\s+$//;
                  my  $key2=$2;$key2 =~ s/^\s+//;$key2 =~ s/\s+$//;
                  my  $key3=$3;$key3 =~ s/^\s+//;$key3 =~ s/\s+$//;
                  my  $key4=$4;$key4 =~ s/^\s+//;$key4 =~ s/\s+$//;
                  my $htmlbodytmp=&GetLogInfo($key1,$key2,$key3,$key4);
                  $htmlbody=$htmlbody.$htmlbodytmp;
              }
       }
        my $html = $htmlhead.$htmlbody.$htmltail;
        #print $html;
        open (my $FILE, ">", $changelog) or die "Can not open $changelog:$!";
        print $FILE $html;
        close $FILE;
}
sub GetLogInfo()
{
        my ($name,$path,$precommit,$nowcommit) = @_;
	print "===$name==$path===\n";
	print "===$precommit===$nowcommit===";
        my $bodytmp="";
        chdir($path);
	print "++++++++++++++";
	if ($precommit ne $nowcommit){
        	print "commitid is difference, need get log\n";
		my $sourcedirtmp=$sourcedir.'/';
		$path=~ s/$sourcedirtmp//;
		print "$path\n";
                if ($changeurl){
                       $bodytmp=$bodytmp.'<tr class="row3"><td colspan="4" rowspan="1"><b>'.$name.'=='.$path.'</b></td></tr>';
		 }else{
		       $bodytmp=$bodytmp.'<tr class="row3"><td colspan="3" rowspan="1"><b>'.$name.'=='.$path.'</b></td></tr>';
                 }
       	#@changeLog=`git log --date=short --no-merges --pretty="%h %ad %an %s" $pcommit..$rcommit`;
        	my @commit=();
		my @commiter=();
		my @msg=();
		if ($precommit eq "addproject"){
			my $number=`ssh -p 29418 $myusername\@$mygerritserver gerrit query --format=json project:$name status:merged branch:$ENV{BRANCH}|jq -r .url|sed 's/null//'|wc -l`;
			chomp($number); 
			print "add projects $name has $number merged changenumbers";
			if ($number == 0){	
				$number = 1;
			}
			print "==============$number===============\n";
			@commit=`git log --date=short --pretty="%h" -$number`;
        		#my @date=`git log --date=short --no-merges --pretty="%ad" $pcommit..$rcommit`;
       			@commiter=`git log --date=short --pretty="%ae" -$number`;
        		@msg=`git log --date=short  --pretty="%s" -$number`;
		}else{
                        @commit=`git log --date=short --pretty="%h" $precommit...$nowcommit`;
                        #my @date=`git log --date=short --no-merges --pretty="%ad" $pcommit..$rcommit`;
                        @commiter=`git log --date=short --pretty="%ae" $precommit...$nowcommit`;
                        @msg=`git log --date=short  --pretty="%s" $precommit...$nowcommit`;
		}
        	for (my $i=0;$i<@commit;$i++)
        	{
			chomp($commit[$i]);
                        if ($changeurl){
				my $url=`ssh -p 29418 $myusername\@$mygerritserver gerrit query --format=json commit:$commit[$i]|jq -r .url|sed 's/null//'|sed '/^\$/d'`;
				chomp($url);
               			print "$url\n";
				#$bodytmp = $bodytmp."<tr><td>$commit[$i]</td><td>$commiter[$i]</td><td>$msg[$i]</td></tr>";
                		$bodytmp = $bodytmp.'<tr class="row4"><td colspan="1" rowspan="1">'.'<a href="'.$url.'" target=_blank">'.$url.'</td><td colspan="1" rowspan="1">'.$commit[$i].'</td><td colspan="1" rowspan="1">'.$commiter[$i].'</td><td colspan="1" rowspan="1">'.$msg[$i].'</td></tr>';
        	       }else{
                             $bodytmp = $bodytmp.'<tr class="row4"><td colspan="1" rowspan="1">'.$commit[$i].'</td><td colspan="1" rowspan="1">'.$commiter[$i].'</td><td colspan="1" rowspan="1">'.$msg[$i].'</td></tr>'
                       }
		}
	}else{
		print "commit id is same, do not need to get log\n";
	}
	#print $bodytmp;
        return $bodytmp
}
&GetChangeList()
