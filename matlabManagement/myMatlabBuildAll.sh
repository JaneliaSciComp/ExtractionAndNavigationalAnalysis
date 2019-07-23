#!/bin/sh
#
# Script to build all the Matlab binaries we needed.  Best practice is to run this on a cluster node,
# e.g. by using qlogin.
MYBASE=/groups/zlatic/zlaticlab/code/extraction_and_navigational_analysis_et_al
MYSOURCE=$MYBASE/matlabSourceLocationForCompilation
MCC=/misc/local/matlab-2012b/bin/mcc
MYOUTDIR=$MYBASE/matlabBinaryLocation

$MCC -v -o processLouis -W main:processLouis -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/processDirectoryStartToFinishSpatial_Louis.m

$MCC -v -o MWTtoMatFiles_Louis -W main:MWTtoMatFiles_Louis -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/processMWTDirectoryToMatfiles_Louis.m

$MCC -v -o combineSpatialCalcs_Louis -W main:combineSpatialCalcs_Louis -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/ \
  -a $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Louis/combineSpatialCalcsFromMultipleDirectoriesForAnalysis_Louis.m

$MCC -v -o processDirToMat -W main:processDirToMat -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/processDirectoryToMatfiles_Janelia.m

$MCC -v -o Spatial -W main:Spatial -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/processDirectoryStartToFinishSpatial_Janelia.m

$MCC -v -o Spatial_Tihana -W main:Spatial_Tihana -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/processDirectoryStartToFinishSpatial_Tihana.m

$MCC -v -o Temporal -W main:Temporal -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/processDirectoryStartToFinishTemporal_Janelia.m


$MCC -v -o CombineSpatialCalcs -W main:CombineSpatialCalcs -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/combineSpatialCalcsFromMultipleDirectoriesForAnalysis.m

$MCC -v -o CombineTemporalCalcs -W main:CombineTemporalCalcs -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/combineTemporalCalcsFromMultipleDirectoriesForAnalysis.m

$MCC -v -o MWTtoMatFiles -W main:MWTtoMatFiles -T link:exe -d $MYOUTDIR \
  -w enable:specified_file_mismatch -w enable:repeated_file -w enable:switch_ignored \
  -w enable:missing_lib_sentinel -w enable:demo_license -v \
  -I $MYSOURCE/Matlab-Track-Analysis \
  -a $MYSOURCE/Matlab-Track-Analysis/useful\ extra\ classes/ \
  -a $MYSOURCE/Matlab-Track-Analysis/utility\ functions/ \
  -a $MYSOURCE/Matlab-Track-Analysis/basic\ routines/ \
  $MYSOURCE/Matlab-Track-Analysis/user\ specific/Janelia/processMWTDirectoryToMatfiles_Janelia.m
