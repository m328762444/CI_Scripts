#!/bin/perl
use strict;
use warnings;
use Cwd;
use Data::Dumper;
use File::Basename;
my $sourcedir=getcwd;
print "$sourcedir\n";
my $filename='.gitmodules';
print "$filename\n";
my %repos = ();
my %precommits = ();
my %nowcommits = ();
my $changelog = $sourcedir."/changelist.html";
print "$changelog\n";
my $precommitfile = $ARGV[0];
my $nowcommitfile = $ARGV[1];
die "$precommitfile is not exist, Please check: $!" unless (-e $precommitfile);
die "$nowcommitfile is not exist, Please check: $!" unless (-e $nowcommitfile);

sub GetModuleRepos()
{       
	chdir($sourcedir) or die "$!";
	my @modulefiles=`find $sourcedir -name $filename`;
	#print "@modulefiles\n";
	my $modulefile = undef;
	#my %repos = ();
	foreach $modulefile(@modulefiles) {
		chomp($modulefile);
		my $pathpre = dirname($modulefile);
		open (my $FILE, "<", $modulefile) or die "Can not open $modulefile:$!";
		my $line = undef;
		my $pathtmp = undef;
		my $urltmp = undef;
		while($line = <$FILE>){
			#print $line;
			if($line =~ /path\s+\=\s+(\S+)/) {
				$pathtmp = $pathpre.'/'.$1;
			}elsif($line =~ /url\s+\=\s+(\S+)/) {
				$urltmp = $1;
				$repos{$urltmp}=$pathtmp;
			}else {
			}		
        	}
      		close $FILE;
	}
}

sub GetMainrepo()
{
	chdir($sourcedir) or die "$!";
	my $mainrepourl = undef;
	my $gitcmd = `git remote -v|grep fetch`;
	if ($gitcmd =~ /\S+\s+(\S+)\s+\S+/) {
		$mainrepourl = $1;
	}	
	$repos{$mainrepourl} = $sourcedir;
}
sub GetCommitInfo()
{
	my ($file,$commithash) = @_ ;
	open (my $FILE, "<", $file) or die "Can not open $file:$!";
        my $line = undef;
        while($line = <$FILE>){
		#print $line;
		if($line =~ /(\S+)\s+\:\s+(\S+)/) {
                        $commithash->{$1} = $2;
			#print "$1===$2"
                }else{
			print "Please Check!!!";
		        print "WaWuWaWuWaWu";
               }
	}
        close $FILE;
        return ($commithash);
}
sub GetChangeList()
{	my $htmlhead = '<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}caption {text-align: left;}td {border: 1px solid black;text-align: left;padding: 8px;}th {border: 1px solid black;text-align: center;padding: 8px;}.row1 {background-color: #0088FF}.row2 {background-color: #DDDD00}.row3 {background-color: #DDDDDD}.row4 { background-color: #FFFFFF }</style></head><body><h2>Stash Change List</h2><table><tr class="row1"><th>Commit ID</th><th>Owner</th><th>CommitMessage</th></tr>';
	my $htmltail = '</body></html>';
	my $htmlbody = "";
	while((my $key, my $value)=each %nowcommits)
	{
		#print "$key==========$value\n";
		#print "$nowcommits{$key}\n";
		if ($precommits{$key} ne $value) {
			#chdir($repos{$key});
			print "commitid is difference, need get log";
			#$repos{$key} $precommits{$key} $nowcommits{$key}
			$htmlbody = $htmlbody.'<tr class="row3"><td colspan="3" rowspan="1"><b>'.$key.'</b></td></tr>';
			my $htmlbodytmp = &GetLogInfo($repos{$key}, $precommits{$key}, $nowcommits{$key});
			$htmlbody = $htmlbody.$htmlbodytmp;
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
	my ($path, $pcommit, $rcommit) = @_;
	my $bodytmp = "";
	chdir($path);
	#@changeLog=`git log --date=short --no-merges --pretty="%h %ad %an %s" $pcommit..$rcommit`;
        my @commit=`git log --date=short --no-merges --pretty="%h" $pcommit..$rcommit`;
        #my @date=`git log --date=short --no-merges --pretty="%ad" $pcommit..$rcommit`;
        my @commiter=`git log --date=short --no-merges --pretty="%ae" $pcommit..$rcommit`;
        my @msg=`git log --date=short --no-merges --pretty="%s" $pcommit..$rcommit`;
	for (my $i=0;$i<@commit;$i++)
        {
               # $bodytmp = $bodytmp."<tr><td>$commit[$i]</td><td>$commiter[$i]</td><td>$msg[$i]</td></tr>";
		$bodytmp = $bodytmp.'<tr class="row4"><td colspan="1" rowspan="1">'.$commit[$i].'</td><td colspan="1" rowspan="1">'.$commiter[$i].'</td><td colspan="1" rowspan="1">'.$msg[$i].'</td></tr>';
        }
	return $bodytmp
}
&GetMainrepo();
&GetModuleRepos();
*precommits = &GetCommitInfo($precommitfile, \%precommits);
*nowcommits = &GetCommitInfo($nowcommitfile, \%nowcommits);
&GetChangeList();
#print Dumper(\%repos);
