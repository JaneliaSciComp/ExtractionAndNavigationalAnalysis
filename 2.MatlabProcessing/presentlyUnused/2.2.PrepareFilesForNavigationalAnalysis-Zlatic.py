# This file symlinks the matfiles generated in the extract part into the Mat-files folder we need. 

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
matFilesDestDir = '/groups/zlatic/zlaticlab/Projects/Zlatic/Mat-files'
#matFilesDestDir = '/groups/larvalolympiad/larvalolympiad/Mat-files-individual'

list_of_files = {}
path = "/groups/zlatic/zlaticlab/pipeline/screen/tracking-results/t1"
njob = 0 ;
for (dirpath, dirnames, filenames) in os.walk(path):
	for filename in filenames:
		# print filename
		if re.match('.*experiment.*\.mat',filename):
			print filename
			print 'we matched!'
			
		# if re.match('\*experiment*\.mat',filename):
		# if filename == 'camcalinfo.mat':
			pathComponents = dirpath.split(os.sep)
			dirLength = len(pathComponents)
			#print pathComponents
			
			destBaseDir = matFilesDestDir #fullProjectDirPath + os.sep + "Mat-files" 
					
			trackingResultsIndex = functions.findTrackingResultsFromPath(pathComponents)
			
			i = trackingResultsIndex+1;
			
			while i < len(pathComponents) - 2 :
				destBaseDir = destBaseDir + os.sep + pathComponents[i]
				i = i + 1


			# print 'destionation dir before loop'
 		# 	print destBaseDir
			
			destBaseDirComponents = destBaseDir.split(os.sep)
			matFilesDir = dirpath # + os.sep + 'matfiles'
			# print matFilesDir
			
			#print 'this is before the matfiles loop'
			for (matFilesPath, matDirName, matFileNames) in os.walk(matFilesDir):
				for matFileName in matFileNames:
					if matFileName[-4:] == '.mat': # we only process .mat files
						
						sourceMatFileName = matFilesPath + os.sep + matFileName
						
						# Let's create symlinks for the individual files
						
						#print matFileName
						
						# we assume it's like this :-)
						dateTime = pathComponents[trackingResultsIndex+4]
						# print pathComponents
						# print dateTime
						
						destIndividualDir = destBaseDir + os.sep + 'individualMatfiles' + os.sep + dateTime + os.sep + 'matfiles' 
						destIndividualFname = destIndividualDir + os.sep + matFileName[:-5] + dateTime + '.mat'
						
						# print sourceMatFileName
						# print destIndividualFname
						# break

						if not os.path.isdir(destIndividualDir): # let's make sure it doesn't exist already
							os.makedirs(destIndividualDir)
						
						
						# if it exists we remove it - for completeness sake :)
 						if os.path.isfile(destIndividualFname):
# 							#print 'File exists!'
 							os.unlink(destIndividualFname)

						# SYMLINKING option						
						# we create the symlink
						print 'Symlinking ' + matFileName
						os.symlink(sourceMatFileName,destIndividualFname)

						
						#print sourceMatFileName
# 						print 'destBaseDir in loop'
# 						print destBaseDir
						
						# because we are getting them directly from the MWT converted...
						destinationFileDir = destBaseDir

						destinationFileName = destBaseDir + os.sep + 'matfiles' + os.sep + matFileName[:-5] + dateTime + '.mat'
						
						
						# print 'destination filename in loop'
 						# print pathComponents[dirLength-1]
 						# print destinationFileName
 						# sys.exit()
						
						
						# first we check if it's already there so we don't copy again - no need!
						if not os.path.isfile(destinationFileName):
	 						#print 'file exists!'
							destinationFileDir = destBaseDir + os.sep + 'matfiles'
							if not os.path.isdir(destinationFileDir): # let's make sure it doesn't exist already
								os.makedirs(destinationFileDir)

							
							#print 'file does not exist, lets copy it'
							#print sourceMatFileName
							#print destinationFileName

							print 'Symlinking ' + matFileName
							os.symlink(sourceMatFileName,destinationFileName)

							#sys.exit()

							#print 'Copying ' + matFileName
							#shutil.copyfile(sourceMatFileName,destinationFileName)
					
					#shutil.copyfile(sourceMatFileName,destinationFileName)
					
						
print 'Done!'						
					


