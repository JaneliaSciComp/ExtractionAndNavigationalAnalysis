# We combine all the analysis files into a new directory containing them all. We will then 
# combine the analysis by running a matlab script
# 2012/01/27
#  This file for now assumes a very well behaved list of files...
# 2012/03/05 - we're shifting to symlinks instead of copying files...
# 2012/03/08 - shifting back to copying **for now** since we can't see those in matlab on the windows computer...
# disabled the individual files. we should make a different script for it
# 2012/03/22 - re-enabled :)
# 2012/06/30 - we're symlinking now

import os
import os.path
import shutil
import sys
import stat
import string
import filecmp



# Combine specific
matFilesDestDir = '/groups/larvalolympiad/larvalolympiad/Mat-files'
#matFilesDestDir = '/groups/larvalolympiad/larvalolympiad/Mat-files-individual'

# print checkerboardsFileNames['t7']
# print checkerboardsFileNames['t8']


def md5_for_file(filename, blockMultiplier):
	import hashlib
	md5 = hashlib.md5()
	while True:
		f = open(filename,'rb')
		data = f.read(blockMultiplier*md5.block_size)
		if not data:
			break
		
#		for chunk in iter(lambda: f.read(blockMultiplier*md5.block_size), ''): 
		md5.update(chunk)
	return md5.digest()


print ''

list_of_files = {}
path = "/groups/larvalolympiad/larvalolympiad/Extracted-files"
njob = 0 ;
for (dirpath, dirnames, filenames) in os.walk(path):
	for filename in filenames:
		if filename == 'camcalinfo.mat':
			pathComponents = dirpath.split(os.sep)
			dirLength = len(pathComponents)
			#print pathComponents
			destBaseDir = matFilesDestDir + os.sep + pathComponents[dirLength-4] + os.sep + \
			pathComponents[dirLength-3] + os.sep + pathComponents[dirLength-2] 
# 			print 'destionation dir before loop'
#  			print destBaseDir
			destBaseDirComponents = destBaseDir.split(os.sep)
			matFilesDir = dirpath + os.sep + 'matfiles'
			#print matFilesDir
			
			#print 'this is before the matfiles loop'
			for (matFilesPath, matDirName, matFileNames) in os.walk(matFilesDir):
				for matFileName in matFileNames:
					if matFileName[-4:] == '.mat': # we only process .mat files
						
						sourceMatFileName = matFilesPath + os.sep + matFileName
						
						# Let's create symlinks for the individual files
						
						#print matFileName
						
						dateTime = pathComponents[dirLength-1]
						
						destIndividualDir = destBaseDir + os.sep + 'individualMatfiles' + os.sep + dateTime + os.sep + 'matfiles' 
						destIndividualFname = destIndividualDir + os.sep + matFileName[:-5] + pathComponents[dirLength-1] + '.mat'
						
						#print sourceMatFileName
						#print destIndividualFname
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

						
						# COPYING MODE
						#if not os.path.isfile(destIndividualFname):
						#	print 'Copying individual ' + matFileName
						#	shutil.copyfile(sourceMatFileName,destIndividualFname)
						#else:
						#	sys.stdout.write('.')
						#	sys.stdout.flush()
						
						
						#sys.exit()
						
						## we copy the matfiles 
# 						if not os.path.isdir(destBaseDir): # let's make sure it doesn't exist already
# 							os.makedirs(destBaseDir)
						
						#print 'source file name in loop'
						
						#print sourceMatFileName
# 						print 'destBaseDir in loop'
# 						print destBaseDir
						
						destinationFileName = destBaseDir + os.sep + 'matfiles' + os.sep + matFileName[:-5] + pathComponents[dirLength-1] + '.mat'
						
						#print destinationFileName

						# print 'destination filename in loop'
#  						print pathComponents[dirLength-1]
#  						print destinationFileName
#  						sys.exit()
						
						# kludgy thing for now - let's just copy the png into the destination folder
						#srcPattern =  matFilesPath[:-8]	+ '*.png'			
						#shutil.copy(srcPattern,destBaseDir)
						srcdir = matFilesPath[:-8]
# 						for basename in os.listdir(srcdir):
# 							if basename.endswith('.png'):
# 								pathname = os.path.join(srcdir, basename)
# 								#print pathname
# 								if os.path.isfile(pathname):
# 									# dstPathName = destBaseDir + os.sep + 'checkerboard.png'
# 									shutil.copyfile(pathname, dstPathName)
						
						
						# first we check if it's already there so we don't copy again - no need!
						if not os.path.isfile(destinationFileName):
	 						#print 'file exists!'
#							sourceHash = md5_for_file(sourceMatFileName,128)
#							print sourceHash
							#print 'Skipped ' + matFileName
# it is very computationally expensive as of now to compare the files (no hash possibility in python 2.4) 
#							if not filecmp.cmp(sourceMatFileName,destinationFileName):
#								print 'file is NOT the same, Copying ' + matFileName
#								shutil.copyfile(sourceMatFileName,destinationFileName)
#							else:
#								print 'Skipped ' + matFileName
							destinationFileDir = destBaseDir + os.sep + 'matfiles'
							if not os.path.isdir(destinationFileDir): # let's make sure it doesn't exist already
								os.makedirs(destinationFileDir)

							
							#print 'file does not exist, lets copy it'
							#print sourceMatFileName
							#print destinationFileName

							print 'Symlinking ' + matFileName
							os.symlink(sourceMatFileName,destinationFileName)

							
							#print 'Copying ' + matFileName
							#shutil.copyfile(sourceMatFileName,destinationFileName)
					
					#shutil.copyfile(sourceMatFileName,destinationFileName)
					
						
print 'Done!'						
					


