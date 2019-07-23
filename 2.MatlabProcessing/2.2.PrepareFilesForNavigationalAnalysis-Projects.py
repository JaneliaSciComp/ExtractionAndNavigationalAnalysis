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

projectsDirs = functions.getProjectDirs(settings.projectsPath)
for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		njob = 0 ;
		for (dirpath, dirnames, filenames) in os.walk(fullProjectDirPath):
			pathComponents = dirpath.split(os.sep)
			tracker = functions.getTrackerName(pathComponents)
			if tracker in settings.rubenTrackers:
				continue
			for filename in filenames:
				if re.match('camcalinfo.mat', filename):
					pathComponents = dirpath.split(os.sep)
					destBaseDir = fullProjectDirPath + os.sep + "Mat-files" 
					startIndex = functions.findIndexOfExtractedFiles(pathComponents)
					i = startIndex+1;
					#TODO fix this
					if re.match('TESTING|TRAINING', pathComponents[len(pathComponents)-1]):
						while i < len(pathComponents) - 2 :
							destBaseDir = destBaseDir + os.sep + pathComponents[i]
							i = i + 1
						destBaseDir = destBaseDir + os.sep + pathComponents[len(pathComponents)-1]
					else:
						while i < len(pathComponents) - 1 :
							destBaseDir = destBaseDir + os.sep + pathComponents[i]
							i = i + 1
					destBaseDirComponents = destBaseDir.split(os.sep)
					matFilesDir = dirpath + os.sep + 'matfiles'
					for (matFilesPath, matDirName, matFileNames) in os.walk(matFilesDir):
						for matFileName in matFileNames:
							if matFileName[-4:] == '.mat': # we only process .mat files
								sourceMatFileName = matFilesPath + os.sep + matFileName
								# Let's create symlinks for the individual files
								if re.match('t14',pathComponents[startIndex+1]) and len(pathComponents)-startIndex > 5:
									dateTime = pathComponents[startIndex+5]
									if re.match('.*\_.*',dateTime):
										# print 'we have an underscore and dateTime is'
										# print dateTime
										m = re.search('(^\d+)\_(.*)',dateTime)
										if m is not None:
											dateTime =  m.group(1)
										else:
											sys.exit('Major error happened')										
									destIndividualDir = destBaseDir + os.sep + 'individualMatfiles' + os.sep + dateTime + os.sep + 'matfiles' 
									destIndividualFname = destIndividualDir + os.sep + matFileName[:-4] + dateTime + '.mat'
								else:
									dateTime = pathComponents[startIndex+4]
									destIndividualDir = destBaseDir + os.sep + 'individualMatfiles' + os.sep + dateTime + os.sep + 'matfiles' 
									destIndividualFname = destIndividualDir + os.sep + matFileName[:-5] + dateTime + '.mat'
								if not os.path.isdir(destIndividualDir): # let's make sure it doesn't exist already
									os.makedirs(destIndividualDir)
								# if it exists we remove it - for completeness sake :) We may have removed it from analysis for example
								# noticed that this unlink doesn't seem to working I wonder if it is because it does not work on broken links?
								if os.path.islink(destIndividualFname):
									os.unlink(destIndividualFname)
								# SYMLINKING option						
								# we create the symlink
								print 'sourceMatFileName: ' + sourceMatFileName
								print 'destIndividualFname: ' + destIndividualFname
								#create symlink if it doesn't exists, though this doesn't help of link is broken
								if not os.path.islink(destIndividualFname):
									os.symlink(sourceMatFileName,destIndividualFname)
								if re.match('TESTING|TRAINING',pathComponents[len(pathComponents)-1]):
									destinationFileName = destBaseDir + os.sep + 'matfiles' + os.sep + matFileName[:-5] + dateTime + '.mat'
								else:
									destinationFileName = destBaseDir + os.sep + 'matfiles' + os.sep + matFileName[:-5] + dateTime + '.mat'
								# we unlink if previously symlinked..
								if os.path.islink(destinationFileName):
									os.unlink(destinationFileName)
								destinationFileDir = destBaseDir + os.sep + 'matfiles'
								if not os.path.isdir(destinationFileDir): # let's make sure it doesn't exist already
									os.makedirs(destinationFileDir)
								print "The link will be:", sourceMatFileName, destinationFileName								
								if not os.path.islink(destinationFileName):
									os.symlink(sourceMatFileName,destinationFileName)
		print 'Done with project ' + fullProjectDirPath					
