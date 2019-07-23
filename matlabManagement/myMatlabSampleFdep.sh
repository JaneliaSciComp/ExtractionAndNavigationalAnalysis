#!/bin/sh
MYSOURCE=/home/epsteinj/samuellab-mirror
#MCC=/misc/local/matlab-2012b/bin/mcc
MATLAB=/misc/local/matlab-2012b/bin/matlab
#MYOUTDIR=$HOME/matlabBinaries
cat >tmp.$$ <<EOF
addpath('$MYSOURCE/Matlab-Track-Analysis/')
addpath('$MYSOURCE/Matlab-Track-Analysis/useful extra classes/')
addpath('$MYSOURCE/Matlab-Track-Analysis/utility functions/')
addpath('$MYSOURCE/Matlab-Track-Analysis/basic routines/')
addpath('$MYSOURCE/Matlab-Track-Analysis/user specific/Janelia/')
addpath('/home/epsteinj/miscMatlabHacks/')
addpath('/home/epsteinj/miscMatlabHacks/hfdep/')
fdep('processDirectoryToMatfiles_Janelia.m')
EOF
$MATLAB -nodisplay <tmp.$$
