#!/bin/sh
#
# Script to build all the Matlab binaries we needed.  Best practice is to run this on a cluster node,
# e.g. by using qlogin.
MYBASE=/groups/zlatic/zlaticlab/code/extraction_and_navigational_analysis_et_al
MYSOURCE=$MYBASE/matlabSourceLocationForCompilationGershowLabBranch
MCC=/misc/local/matlab-2012b/bin/mcc
MYOUTDIR=$MYBASE/matlabBinaryLocation

$MCC -v -o processDirToMatRuben -W main:processToMatfilesRuben -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ruben/ \
  -a $MYSOURCE/Matlab-Track-Analysis/yamlMatlab/ \
  -a $MYSOURCE/Matlab-Track-Analysis/SemiAutomaticAnalysis/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ruben/processToMatfiles_Gepner.m