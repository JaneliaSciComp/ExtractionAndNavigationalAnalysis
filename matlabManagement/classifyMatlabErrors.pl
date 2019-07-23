use strict;
use File::Find;

my $basedir = "/groups/zlatic/zlaticlab/Projects/jobs.ignore/matlab/"; #TEMP
my $basedir;
my %classes;
my %errorFree;
my $classNum = 0;
my $totalErroneous;
my %hoA;
my %trackers;

my $inpList = shift @ARGV or die "Expected list of log files as 1st parameter";
my $tooNewTimestamp = shift @ARGV or die "Expected timestamp-file as 2nd parameter";
my $staleDays = shift @ARGV || 30;

my $mTime = -M $tooNewTimestamp;
my %foundFiles;
my %hasNewFiles;
my %logsWithNewAssociatedData;

my $maxNewFilesToPrint = 3;

open INP,"<$inpList" or die "Unable to open $inpList";

while (<INP>) {
	chomp;
	my $fname = $basedir . $_;
	my $errorString;
	my $offendingProcess;
	open F,"<$fname" or die "Unable to open input $fname";
	my @contents = <F>; # slurp
	close F;
	foreach my $line (@contents) {
		if ($line =~ /LD_LIBRARY_PATH/) {
			$errorString = "";
		}
		if ($line =~ /^Error/ || $line =~ /^MATLAB/ || $line =~ /^Output argument/) {
			$line =~ s#/.*/##g; # Eliminate all pathnames which might make matters non-unique
			$errorString .= $line;
			if ($line =~ /^Error in ([process|combine]\w+)/) {
				$offendingProcess = $1;
			} elsif ($line =~ /errorDocCallback\('(\w+)/) {
				$offendingProcess = $1;
			}
		}
	}
	if ($errorString) {
		if ($offendingProcess) {
			$errorString = "**$offendingProcess**\n" . $errorString;
		}
		unless (defined($classes{$errorString})) {
			$classes{$errorString} = $classNum;
		}
		push(@{$hoA{$errorString}}, $fname);
		$totalErroneous++;
	} else {
		$errorFree{$fname}++;
		$errorString = "ERROR-FREE";
	}

	my $shFname = $fname;
	$shFname =~ s/\.log$//;
	$shFname .= ".sh";
	open F,"<$shFname" or die "Unable to open log file's shell-script companinion $shFname";
	my @contents = <F>; # slurp
	close F;
	my $tracker;
	foreach my $line (@contents) {
		if ($line =~ /[^\\] .*\/(t\d+)[\\]\//) {
			$tracker = $1;
			$trackers{$errorString}{$tracker}++;
			if ($line =~ /\/usr\/local\/matlab[^ ]* (.*)/) {
				my $rest = $1;
				my $first = $rest;
				$first =~ s/[^\\] .*//; # looking for a blank preceded by a non-backslash
#				print STDERR "FIRST $first\n";
				open F2,"echo $first |" or die "Unable to process command echo \"$first\"";
				my $cleaned = <F2>;
				chomp $cleaned;
				$cleaned =~ s/\\@/@/g; # at-signs seem to be problematic
				close F2;
				if (-d "$cleaned") {
#					print STDERR "$cleaned IS a valid directory\n";
					%foundFiles = ();
					find(\&wanted,$cleaned);
					my $count = scalar (keys %foundFiles);
					if ($count > 0) {
						$logsWithNewAssociatedData{$errorString}++;
						foreach my $foundFile (keys %foundFiles) {
							$hasNewFiles{$fname}{$foundFile}++;
							print STDERR "Post-processing wanted: $foundFile\n" if printif($foundFile);
						}
					}
				} else {
					print STDERR "$cleaned is NOT a valid directory\n";
					print STDERR "$line\n";
				}
			}
		}
	}
}
close INP;

my $errorClassCount = scalar keys %classes;
my $errorFreeCount = scalar keys %errorFree;
print "Error-free logfiles: (there were $errorClassCount classes of errors, $errorFreeCount error-free logfiles, and $totalErroneous error-containing logfiles)\n";
foreach (sort keys %errorFree) {
	print "  $_\n";
}

my $classNum = 0;
foreach my $errorString (sort keys %classes) {
	my $trackersString;
	foreach my $tracker (sort keys %{$trackers{$errorString}}) {
		$trackersString .= "," if $trackersString;
		$trackersString .= $tracker;
	}
	my $hasNewAssociatedData = $logsWithNewAssociatedData{$errorString} ? "HAS NEW DATA; " : "LACKS NEW DATA; ";
	print "\n\n\n(${hasNewAssociatedData}TRACKERS: $trackersString)\nERROR CLASS $classNum, representative error string:\n\n";
	$classNum++;
	print "$errorString;\n\n";
	foreach my $fname (sort @{$hoA{$errorString}}) {
                my $haveNewFiles = defined($hasNewFiles{$fname});
		print "  $fname";
		print "  ***" if $haveNewFiles;
		print "\n";
		print "    " . examineMatFilesStatus($fname) . "\n";
		if ($haveNewFiles) {
			my $i = 1;
			foreach my $foundFile (sort keys %{$hasNewFiles{$fname}}) {
				last if $i++ > $maxNewFilesToPrint;
				print "    NEW: $foundFile\n";
			}
		}
	}
}


sub examineMatFilesStatus {
        my ($logFname) = @_;
	$_ = $logFname;
        s/\.log$//;
        my $shFname = $_ . ".sh";
        my $retval = "";

        if (open F,"<$shFname") {
#print "Opened $shFname\n";
                while (<F>) {
                        chomp;
                        if (/individualMatfiles/i) {
#print "  matched individualMatFiles $_\n";
                                # the following backquoted Perl invocation is a hack to extract the third command-line
                                # argument without worrying about backslashes
                                my $dirName = `perl -e '{ print \$ARGV[2]; }' $_`;
                                $dirName .= "/matfiles/";
#print "Attempting to open $dirName";
                                if (opendir(my $dh, $dirName)) {
#print "opendir $dirName succeeded";
                                        my @matlabSymlinks = grep { -l "$dirName/$_" } readdir($dh);
                                        foreach my $link (@matlabSymlinks) {
                                                $link = "$dirName/$link";
                                                $retval .= "  Following $link  ";
                                                my $followedLink;
                                                if ($followedLink = readlink $link) {
                                                        my $fileSize = -s $followedLink;
                                                        $retval .= "->  $followedLink ($fileSize bytes) ";
                                                } else {
                                                        $retval .= "->  $followedLink (Broken link)";
                                                }
                                        }
                                        closedir $dh;
                                }
                        }
                }
        }

        return $retval;
}



sub wanted {
	my $pathName = $File::Find::name;

	return unless -f $pathName;
	my $thisMtime = -M $pathName;
	return if $thisMtime < $mTime; # this file is too new to be counted
#	print STDERR "IN wanted: $pathName\n";
#	print STDERR "$thisMtime,$mTime,$staleDays\n";
	return if $thisMtime > ($mTime + $staleDays);
	print STDERR "In wanted: $pathName\n" if printif($pathName);
	$foundFiles{$pathName}++;
}

sub printif {
	return /t1_p_3gradient/;
}

