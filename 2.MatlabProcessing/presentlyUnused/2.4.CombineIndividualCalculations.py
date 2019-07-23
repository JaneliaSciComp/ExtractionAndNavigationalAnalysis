# 20121114 - Combining calculations here

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
	f.write(script + ' ' + mcrLocation + ' ' + expDir + '/' + '\n')  
	f.write('rm -rf $MCR_CACHE_ROOT \n')
	f.close 
	os.chmod(shfile,0744)
	return


def CombineCalculationsinDirectory(tracker, directory):
	
	# our own settings file!
	

	#print 'in the analyzeDir'
	#print tracker
	 

	# create the line handle from directory
	directoryComp = str.split(directory,os.sep)
	#print directoryComp
	
	if directoryComp[len(directoryComp)-2] == 'individualMatfiles':
		print 'It is an individual run, exiting!'
		sys.exit() # we should NEVER see this
		
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
	shfile = settings.batchScriptDir + 'CombineCalculations/CombineCalcs_' + tracker + '_' + normLineHandle + '.sh'
	#print shfile
	
	expParameters = cmdLineName + ' runningOnCluster 1 '
	
	normDirectory = string.replace(directory,'@','\@')
	
	
	
	# we only run it on Spatial stuff for now
	pat = re.compile('t7|t9|t10|t8')
	controlsPat = re.compile('FCF_|ywr')
	if pat.match(tracker) :
		createQsubFile(shfile,settings.mcrLocation,settings.CombineCalcs[tracker],normDirectory,expParameters) 
		qsubAdditional = ' -pe batch 1'
		if controlsPat.match(lineName[:4]):
			qsubAdditional = ' -pe batch 16'

	else:
		return

	
	jobName = 'combCalc_' + tracker + '_' + normLineHandle ;
	
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
		if re.match(matDirName,'matfiles'): # we only process if we have a folder with .mat files - Even though we don't care about them here
			print matFilesPath
			
			#print 'we have matfiles'

			# Now we check if it's not an individual because we are not interested in that

			calculationsFullPath =  matFilesPath + os.sep + 'calculations'
			matFilesPathComp = str.split(matFilesPath,os.sep)
			ti = functions.findTrackerFromPath(matFilesPathComp)
			tracker = matFilesPathComp[ti+1]
			# print tracker
			
			possibleIndividualDir = matFilesPathComp[len(matFilesPathComp)-2]
			
			# By default we don't run the combination of analysis..
			mustRun = False
			
			if not re.search(possibleIndividualDir,'individualMatfiles'):

				# If the directory does not exist, we combine the calculations
				if not os.path.isdir(calculationsFullPath):
					print calculationsFullPath
					print matFilesPath
					print 'folder does not exist so we do the whole thing-a-mop!'
					functions.writeCombMatfileList(matFilesPath)						
					# raw_input('Folder does not exist so we write combfiles.txt...')
					# mustRun	= True
					functions.CombineCalculationsinDirectory(tracker,matFilesPath)

					#sys.exit()

				elif os.path.isdir(calculationsFullPath):
					
					print calculationsFullPath
					


					# first we check if there's a matfile. If there's not, we re-run the combine analysis yo
					analysisFilePresent = False
					for (calcPath, calcDir, calcFnames) in os.walk(calculationsFullPath):
						for calcFname in calcFnames:
							if re.match('.*analysis\.mat',calcFname):
								print 'we found an analysis file!'
								analysisFilePresent = True
							# print calcFname

					# if analysisFilePresent:
					# 	raw_input('analysis file present')

					
					mustReRun = functions.checkCombMatfileList(matFilesPath)

					print mustReRun
					print analysisFilePresent
					print matFilesPath

					# raw_input('We found a directory called calculations')							

					# We now run it if the analysis file is not present or there are newer files
					#if not (analysisFilePresent or mustReRun):
					if mustReRun or not analysisFilePresent:

						# writeCombMatfileList(matFilesPath)						
						# CombineCalculationsinDirectory(tracker,matFilesPath)
						print 'we are running it yo'

						print 'mustReRun'
						print mustReRun
						print 'analysisFilePresent'
						print analysisFilePresent
						print matFilesPath
						# raw_input('We are running the combination!')
						# sys.exit()
						#raw_input('oh yeah')
						functions.writeCombMatfileList(matFilesPath)	
						functions.CombineCalculationsinDirectory(tracker,matFilesPath)


		# if matDirName == 'matfiles': # we only process if we have a folder with .mat files - Even though we don't care about them here
			
		# 	if os.path.isdir(matFilesPath + os.sep + 'calculations'):
		# 		#print 'Skipping ' + matFilesPath
		# 		b=0
		# 		a = b
		# 	else:
		# 		#sys.exit()
		# 		print '\r\n' + '------ ' + 'Combining calculations in ' + matFilesPath + ' ------ '
		# 		matFilesPathComp = str.split(matFilesPath,os.sep)
				
		# 		# we need to identify the tracker based on the file structure...
		# 		#if os
				
		# 		informativeDir = matFilesPathComp[len(matFilesPathComp)-2]
		# 		#print informativeDir
		# 		if informativeDir == 'individualMatfiles':
		# 			#print 'It is!'
		# 			trackerID = matFilesPathComp[len(matFilesPathComp)-5]
		# 		else:
		# 			trackerID = matFilesPathComp[len(matFilesPathComp)-3]
		# 			CombineCalculationsinDirectory(trackerID,matFilesPath)	
				
		# 		#print trackerID
				
				
		# 		#sys.exit()



