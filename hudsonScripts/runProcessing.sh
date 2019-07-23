#!/bin/sh

#Decide if in testing environment or not
TEST=false
ZLATIC=false
alias py=/misc/local/python-2.7.1/bin/python
while getopts tz OPTION
do
    case ${OPTION} in
        t) TEST=true;;
        z) ZLATIC=true;;
        \?) echo "bad argument";exit 1;;
    esac
done
#
#. /sge/current/default/common/settings.sh
# setup LSF
. /misc/lsf/conf/profile.lsf
#export DRMAA_LIBRARY_PATH="$SGE_ROOT/lib/lx-amd64/libdrmaa.so"
source /groups/flyprojects/home/olympiad/SOURCEME

if [ $TEST = true ]
then
    WORKSPACE='/home/umayaml/bin/LarvalOlympiad/ExtractionAndNavigationalAnalysisEtAl'
    pipeline_dir="$WORKSPACE/trunk/test/Projects/"
    zlatic_dirs="['$WORKSPACE/trunk/test/tracking-results/t11', '$WORKSPACE/trunk/test/tracking-results/t1']"
    zlatic_cluster_scripts="$WORKSPACE/trunk/test/Projects/jobs.ignore/"
    JANELIA_USE_NIGHT_QUEUE=false
elif [ $ZLATIC = true ]
then
    pipeline_dir="/groups/zlatic/zlaticlab/Projects/"
    #zlatic_dirs="['/groups/zlatic/zlaticlab/pipeline/screen/tracking-results/t1', '/groups/zlatic/zlaticlab/pipeline/rd/tracking-results/t1']"
    zlatic_dirs="['/groups/zlatic/zlaticlab/pipeline/screen/tracking-results/t1']"
    zlatic_cluster_scripts="/groups/zlatic/zlaticlab/ClusterJobs/matlab/"
else
    #/groups/zlatic/zlaticlab/from_tier2/larvalolympiad
    #pipeline_dir="/groups/larvalolympiad/larvalolympiad/Projects/"
    pipeline_dir="/groups/zlatic/zlaticlab/larvalolympiad/Projects/"
    #zlatic_dirs="['/groups/larvalolympiad/larvalolympiad/pipeline/screen/tracking-results/t11']"
    zlatic_dirs="['/groups/zlatic/zlaticlab/larvalolympiad/pipeline/screen/tracking-results/t11', '/groups/zlatic/zlaticlab/larvalolympiad/pipeline/screen/tracking-results/t110']"
    zlatic_cluster_scripts="/groups/zlatic/zlaticlab/ClusterJobs/matlab/"
fi

umask 002


#touch larval.timestamp.$$
cd $WORKSPACE/trunk 
find . -name \*.sh | xargs chmod 775
settings_dir=`pwd`/settings/

# there are some executables in the settings directory, so let's throw up our hands and make
# all the files in that directory executable
chmod 775 $settings_dir/*
py $settings_dir/config_maker.py --settings_dir $settings_dir --pipeline_dir $pipeline_dir --zlatic_dirs "$zlatic_dirs" --zlatic_cluster_scripts $zlatic_cluster_scripts
mkdir -p $pipeline_dir/jobs.ignore/matlab/CombineCalculations
mkdir -p $pipeline_dir/jobs.ignore/matlab/navigationalAnalysis
mkdir -p $pipeline_dir/jobs.ignore/matlab/toMatFiles


# remove some file debris
if [[ $TEST != true ]]
then
    echo "Not testing"
	for MatFilesDir in  $pipeline_dir/*/Mat-files
	do
		echo "Looking for file debris in " $MatFilesDir
            #find $MatFilesDir -type l -! -exec test -e {} \; -print
	        #find $MatFilesDir -type l ! -exec test -r {} \; -print | perl hudsonScripts/removeStraySymlinksAndCleanup.pl
	done
fi

function error_exit
{
    echo "$1" 1>&2
    exit 1
}

cd 1.Extraction
pwd
echo "Before step 1.1" at `date`
##py 1.1.ExtractMMF-Projects.py || error_exit "Step 1.1 failed, exiting."
#/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r
#echo "Before step 1.1 Ruben Specific" at `date`
#py 1.1.ExtractMMF-Ruben.py || error_exit "Step 1.1 (Ruben) failed, exiting."
#/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r
cd  ../2.MatlabProcessing
#
#echo "Before step 2 Ruben Specific" at `date`
#py 2.CreateMatfilesAndAnalysis-Ruben.py || error_exit "Step 2 (Ruben) failed, exiting"
echo "Before step 2.1" at `date`

##py 2.1.CreateMatFilesJobs-Projects.py || error_exit "Step 2.1 failed, exiting."
##/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r

echo "Before step 2.1 Zlatic-specific"
py 2.1.CreateMatFilesJobs-Zlatic.py || error_exit "Step 2.1 (Zlatic-specific) failed, exiting."
/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r

echo "Before step 2.2" at `date`
py 2.2.PrepareFilesForNavigationalAnalysis-Projects.py || error_exit "Step 2.2 failed, exiting."

echo "Before step 2.2 Zlatic-specific" at `date`
py 2.2.PrepareFilesForNavigationalAnalysis-Zlatic.py || error_exit "Step 2.2 Zlatic-specific failed, exiting."

echo "Before step 2.3, 1st of two" at `date`
py 2.3.ProcessNavigationalAnalysisJobs-Projects.py || error_exit "Step 2.3 (first) failed, exiting."
/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r

echo "Before step 2.4" at `date`
py 2.4.CombineIndividualCalculations-Projects.py || error_exit "Step 2.4 failed, exiting."
/groups/zlatic/zlaticlab/code/choreography_plots/check_bjobs.pl -t 20 -l -r

#repeat step 2.3
echo "Before step 2.3, 2nd of two" at `date`
py 2.3.ProcessNavigationalAnalysisJobs-Projects.py || error_exit "Step 2.3 (second) failed, exiting."
echo "Processing complete!" at `date`


