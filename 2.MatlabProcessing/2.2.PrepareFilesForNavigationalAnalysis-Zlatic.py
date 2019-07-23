# This file symlinks the matfiles generated in the extract part into the Mat-files folder we need. 

import os
import os.path
import shutil
import sys
import stat
import string
import filecmp
import re

sys.path.append('../settings')
import settings
import functions

matFilesDestDir = settings.mainProjectsPath + '/Zlatic-Like/Mat-files'
list_of_files = {}
projectDirs = functions.getProjectDirs(settings.zlaticProjectsPath)
njob = 0 ;
for path in projectDirs:
	for (dirpath, dirnames, filenames) in os.walk(path):
		pathComponents = dirpath.split(os.sep)
		tracker = functions.getTrackerName(pathComponents)
		if tracker in settings.rubenTrackers:
			continue
		for filename in filenames:
			if re.match('.*experiment.*\.mat',filename):
				pathComponents = dirpath.split(os.sep)
				dirLength = len(pathComponents)
				destBaseDir = matFilesDestDir #fullProjectDirPath + os.sep + "Mat-files" 
				trackingResultsIndex = functions.findTrackingResultsFromPath(pathComponents)
				i = trackingResultsIndex+1;
				while i < len(pathComponents) - 2 :
					destBaseDir = destBaseDir + os.sep + pathComponents[i]
					i = i + 1
				destBaseDirComponents = destBaseDir.split(os.sep)
				matFilesDir = dirpath # + os.sep + 'matfiles'
				for (matFilesPath, matDirName, matFileNames) in os.walk(matFilesDir):
					for matFileName in matFileNames:
						if matFileName[-4:] == '.mat': # we only process .mat files
							sourceMatFileName = matFilesPath + os.sep + matFileName
							dateTime = pathComponents[trackingResultsIndex+4]
							destIndividualDir = destBaseDir + os.sep + 'individualMatfiles' + os.sep + dateTime + os.sep + 'matfiles' 
							destIndividualFname = destIndividualDir + os.sep + matFileName[:-5] + dateTime + '.mat'
							if not os.path.isdir(destIndividualDir): # let's make sure it doesn't exist already
								os.makedirs(destIndividualDir)
							# if it exists we remove it - for completeness sake :)
	 						if os.path.islink(destIndividualFname):
	# 							#print 'File exists!'
	 							os.unlink(destIndividualFname)
							# SYMLINKING option						
							# we create the symlink
							if not os.path.islink(destIndividualFname):
								os.symlink(sourceMatFileName, destIndividualFname)

							destinationFileDir = destBaseDir
							destinationFileName = destBaseDir + os.sep + 'matfiles' + os.sep + matFileName[:-5] + dateTime + '.mat'
							# first we check if it's already there so we don't copy again - no need!
							if not os.path.isfile(destinationFileName):
		 						#print 'file exists!'
								destinationFileDir = destBaseDir + os.sep + 'matfiles'
								if not os.path.isdir(destinationFileDir): # let's make sure it doesn't exist already
									os.makedirs(destinationFileDir)
								if not os.path.islink(destinationFileName):
									os.symlink(sourceMatFileName, destinationFileName)
	print 'Done!'						
						
	
	
