#!/bin/bash
# script for execution of deployed applications
#
# Sets up the MCR environment for the current $ARCH and executes 
# the specified command.
#
export MCR_CACHE_ROOT="/scratch/afonsob";
export XAPPLRESDIR="$matlabroot/X11/app-defaults" ;
export MCR_INHIBIT_CTF_LOCK=1;

./Directional test/ eset checkerboardfname t7_checkerboard_20120119.png