# going to skip the directory if there is a calculations folder

# 04/12/12 - we're not doing calculations for the controls, the FCF_attp2
# 20121114 - We're now skipping global lines. We only process individual files and then we combine them

import os
import os.path
import shutil
import sys
import stat
import string
import filecmp
import re

sys.path.append('/groups/larvalolympiad/home/afonsob/BrunoAnalysis/settings/current')
import settings
import functions



# Combine specific
matFilesDestDir = '/groups/larvalolympiad/larvalolympiad/Mat-files'


# print checkerboardsFileNames['t7']
# print checkerboardsFileNames['t8']


# we create a file this way :)
def createQsubFile(shfile, mcrLocation, script, expDir, expParameters):
	f = open(shfile, 'w')
	f.write('#!/bin/bash \n')
	f.write('\n')
	f.write('# This script will be qsubbed\n')
	from time import gmtime, strftime
	#mcrCacheRoot = '/scratch/afonsob/navAnalysis_' + strftime("%Y%m%d%H%M%S", gmtime()) ;


#	mcrCacheRoot = string.replace(mcrCacheRoot,'@','_') 
#	mcrCacheRoot = string.replace(mcrCacheRoot,'-','_') 
	
	#f.write('export MCR_CACHE_ROOT=' + mcrCacheRoot + '\n\n')
	mcrCacheRoot = '/scratch/afonsob/navMatFile' ;
	f.write('export MCR_CACHE_ROOT=' + mcrCacheRoot + '.$JOB_ID \n\n')
	#f.write('export MCR_CACHE_ROOT=/scratch/mcr_cache_root \n\n')
	f.write('echo `date` \n\n')
	f.write('echo $MCR_CACHE_ROOT \n\n')
	f.write('export MCR_INHIBIT_CTF_LOCK=1\n')
	f.write(script + ' ' + mcrLocation + ' ' + expDir + ' ' + expParameters + '\n')  
	f.write('rm -rf $MCR_CACHE_ROOT \n')
	f.close 
	os.chmod(shfile,0744)
	return


def analyzeDirectory(tracker, directory):
	
	# our own settings file!
	import settings

	#print 'in the analyzeDir'
	#print tracker
	 

	# create the line handle from directory
	directoryComp = str.split(directory,os.sep)
	#print directoryComp
	
	if directoryComp[len(directoryComp)-2] == 'individualMatfiles':
		#print 'It is an individual run!'
		lineName = directoryComp[len(directoryComp)-4] + '_' + directoryComp[len(directoryComp)-1]
		#mcrCacheRoot = settings.mcrCacheRootBase  + tracker + '_' + string.replace(lineName,'@','_')  
	else:
		#print 'it is not'
		
		lineName = directoryComp[len(directoryComp)-2]
		# For now lets skip the FCF controls marc analysis via matlab
		# UNCOMMENT THIS TO NOT PROCESS THE CONTROLS
#		if lineName[:4]=="FCF_":
#			return
			
#			print 'aqui fazemos escape pa'
#			print lineName
			
		#mcrCacheRoot = settings.mcrCacheRootBase  + tracker + '_' + string.replace(lineName,'@','_')
	
	
	
#	return
	
	#print mcrCacheRoot

	
	normLineHandle = string.replace(lineName,'#','_')
	normLineHandle = string.replace(normLineHandle,'@','_')
	cmdLineName = lineName 
	#cmdLineName = string.replace(lineName,'@','\@') ;
	
	
	# Create the .sh file
	shfile = settings.batchScriptDir + 'navigationalAnalysis/matlabNavAnalysis_' + tracker + '_' + normLineHandle + '.sh'
	#print shfile
	
	expParameters = cmdLineName + ' runningOnCluster 1 '
	
	normDirectory = string.replace(directory,'@','\@')
	createQsubFile(shfile,settings.mcrLocation,settings.matlabScriptAnalysis[tracker] ,normDirectory,expParameters) 
	
	pat = re.compile('t7|t9|t10')
	controlsPat = re.compile('FCF_|ywr')
	if pat.match(tracker) :
	#if tracker == ("t7" or "t9" or "t10") :
		matlabFileName = 'Spatial'
		qsubAdditional = ' -pe batch 1'
		if controlsPat.match(lineName[:4]):
			qsubAdditional = ' -pe batch 16'

	elif tracker == "t8" :
		matlabFileName = 'Temporal'
		qsubAdditional = ' -pe batch 3'
		if controlsPat.match(lineName[:4]):
			qsubAdditional = ' -pe batch 16'

	
	jobName = 'nav_' + tracker + '_' + normLineHandle ;
	
	#jobName = pathComponents[dirLength-3] + '_' + pathComponents[dirLength-2] + '_' + pathComponents[dirLength-1]\
	#+ 
	
	qsubOut = shfile[:-3] + '.log'
	
	qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
	print qsubCommand
	
	
	os.system(qsubCommand)	
	#os.remove(shfile)
	#sys.exit()

	
	return
	

	
list_of_files = {}

# We run now the qsubbing for Mat-directories!
for (matFilesPath, matDirNames, matFileNames) in os.walk(matFilesDestDir):
	for matDirName in matDirNames:

		if re.match('matfiles',matDirName): # we only process if we have a folder with .mat files

			# print tracker 

			# individual files are always closer to the end. First we check if it is an individual dir. If it's not, 
			# we see if an analysis file already exists or not. If so, do not run
			matFilesPathComp = str.split(matFilesPath,os.sep)
			possibleIndividualDir = matFilesPathComp[len(matFilesPathComp)-2]

			calcDir = matFilesPath + os.sep + 'calculations'


			# If it's an individual run and there's no calculations, just run it baby
			if re.match('individualMatfiles',possibleIndividualDir) and not os.path.isdir(calcDir) :
				# print 'It is!'
				# print matFilesPathComp
				# break
				print '\r\n' + '------ ' + 'Processing ' + matFilesPath + ' ------ '
				# print tracker
				# print matFilesPath
				# break
				matFilesPathComp = str.split(matFilesPath,os.sep)
				
				# print matFilesPathComp
				i = functions.findTrackerFromPath(matFilesPathComp)
				# print matFilesPathComp[i]
				tracker = matFilesPathComp[i+1]
				analyzeDirectory(tracker,matFilesPath)

			
			# else - a global analysis file - if there is not a calculations file, we don't run it, because we will combine it
			elif os.path.isdir(calcDir):
				
				analysisFilePresent = False
				
				# First we find if there is a an analysis file present previously combined
# LOOK HERE!! ->>					####################  We could probably optimize this a lot :-)
				# t = time.time()
				for (analysisFilesPath, analsysDirNames, analysisFileNames) in os.walk(calcDir):
					for analysisFileName in analysisFileNames:
						if re.match('.*analysis.mat',analysisFileName):
							analysisFilePresent = True
				
				# elapsed = time.time() - t
				# print elapsed

				figuresDir = matFilesPath + os.sep + 'figures'
				figurePresentFile = figuresDir + os.sep + 'simpleMetrics.pdf'
				
				# If there's not figures directory but analysis is present, we run it
				if not os.path.isdir(figuresDir) and analysisFilePresent:
					# print 'we run the analysis'
					# print calcDir
					
					matFilesPathComp = str.split(matFilesPath,os.sep)
					
					# print matFilesPathComp
					i = functions.findTrackerFromPath(matFilesPathComp)
					# print matFilesPathComp[i]
					tracker = matFilesPathComp[i+1]
					analyzeDirectory(tracker,matFilesPath)	
					# raw_input("There's no figure directory !")

				# if the figures folder is present as well as the analysis file, we see if we need to rerun the figure making
				# figuresFilePresent = False
				
				elif os.path.isdir(figuresDir) and analysisFilePresent and not os.path.isfile(figurePresentFile):
					# print 'we run the analysis'
					# print calcDir
					matFilesPathComp = str.split(matFilesPath,os.sep)
					
					# print matFilesPathComp
					i = functions.findTrackerFromPath(matFilesPathComp)
					# print matFilesPathComp[i]
					tracker = matFilesPathComp[i+1]
					analyzeDirectory(tracker,matFilesPath)	




			# if os.path.isdir(matFilesPath + os.sep + 'calculations'):
			# 	print 'Skipping ' + matFilesPath
			# else:
			# 	#sys.exit()
			# 	#print '\r\n' + '------ ' + 'Processing ' + matFilesPath + ' ------ '
			# 	matFilesPathComp = str.split(matFilesPath,os.sep)
				
			# 	# we need to identify the tracker based on the file structure...
			# 	#if os
				
			# 	informativeDir = matFilesPathComp[len(matFilesPathComp)-2]
			# 	#print informativeDir
			# 	if informativeDir == 'individualMatfiles':
			# 		#print 'It is!'
			# 		print matFilesPathComp
			# 		print '\r\n' + '------ ' + 'Processing ' + matFilesPath + ' ------ '
			# 		trackerID = matFilesPathComp[len(matFilesPathComp)-5]
			# 		analyzeDirectory(trackerID,matFilesPath)
			# 	else: # we now skip these..
			# 		trackerID = matFilesPathComp[len(matFilesPathComp)-3]	
				
			# 	#print trackerID
				
				
			# 	#analyzeDirectory(trackerID,matFilesPath) # we now skip globally submitting these
			# 	#sys.exit()



