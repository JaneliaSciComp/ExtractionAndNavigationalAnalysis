#!/usr/bin/perl
use strict;
use File::Find;
#use File::Path 'remove_tree';
use File::Path 'rmtree';

my @e1;
my $errlist1;
$errlist1 = \@e1;
my $errlist2;

my $errlistref1 = \$errlist1;

# Expects standard-input containing a list of broken symlinks, such as what is produced by:
#    find . -type l ! -exec test -r {} \; -print
#
#
# If the symlink's complete path is of the form: 
#   /individualMatfiles.*.mat/
#    then remove that subdir individualMatfiles/THISDIR
#
#    else:
#       just remove the .mat file
#
#
#
#
#  In general, if you remove ANY file (above), then if the parent directory is empty then remove the parent & proceed recursively upwards in the directory
#
#
#  But: if the directory is named "matfiles" then delete its parent directory and all of its contents
#
#

sub is_folder_empty {
	opendir my $dh, +shift or die $!;
	return not grep { not /^\.+$/ } readdir $dh;
}

sub common_prefix {
        my $comm = shift @_;
        while ($_ = shift @_) {
            $_ = substr($_,0,length($comm)) 
                if (length($_) > length($comm));
            $comm = substr($comm,0,length($_)) 
                if (length($_) < length($comm));
            if (( $_ ^ $comm ) =~ /^(\0*)/) {
                $comm = substr($comm,0,length($1));
            } else {
                return undef;
            }
        }
        return $comm;
}

sub delete_dir_and_parent_as_needed {
	my $path = $File::Find::name;
#	print "In delete_dir function, path=$path, filename=$_\n";
        if (-d $path && is_folder_empty($path)) {
		print "Removing empty folder $path\n";
		rmdir $path;
		if (/^(.*)\/matfiles$/) {
			my $parentDir = $1;
			print "Removing parent of matfiles directory, $parentDir\n";
			rmtree($parentDir, { verbose => 1, error => $errlistref1 } );
		}
	}
}

my $linenum = 0;
my $commonPrefix;
while (<>) {
	chomp;
	if ($linenum++) {
		$commonPrefix = common_prefix($_,$commonPrefix);
	} else {
		$commonPrefix = $_;
	}
	my $file = $_;
	next unless -l $file;
	if ($file =~ /(^.*individualMatfiles\/)([^\/]*).*.mat/) {
		my $candidateSubdirForDeletion = "$1$2";
		print "Planning to remove subdir $candidateSubdirForDeletion\n";
		rmtree($candidateSubdirForDeletion, { verbose => 1, error => \$errlist2 } );
	} else {
		print "Planning to remove individual file $file\n";
		unlink $file;
	} 
}

#finddepth(sub { { print Removing $_; rmdir $_ } if -d $_ && is_folder_empty($_)}, $some_path);
print "Preparing to prune folder $commonPrefix\n";
finddepth(\&delete_dir_and_parent_as_needed,$commonPrefix);


if (@$errlist1) {
      print "errlist1\n";
      for my $diag (@$errlist1) {
          my ($file, $message) = %$diag;
          if ($file eq '') {
              print "general error: $message\n";
          }
          else {
              print "problem unlinking $file: $message\n";
          }
      }
  }

