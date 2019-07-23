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
import re


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

individualPat = re.compile('individualMatfiles')
analysisPat = re.compile('spatial_analysis.mat|temporal_analysis.mat')

print ''

list_of_files = {}
path = "/groups/larvalolympiad/larvalolympiad/Mat-files"
njob = 0 ;
for (dirpath, dirnames, filenames) in os.walk(path):
	for filename in filenames:
		if analysisPat.match(filename):
			pathComponents = dirpath.split(os.sep)
			dirLength = len(pathComponents)
			#print pathComponents

			
			if individualPat.match(pathComponents[dirLength-3]) :
				#print 'It is individual'
				destBaseDir = (os.sep).join(pathComponents[:-3]) + os.sep + 'individualCalculations'
 				#print 'destination dir before loop'
  				#print destBaseDir
				
				dateTime = pathComponents[dirLength-2]
				#print dateTime
				
				destIndividualFname = destBaseDir + os.sep + pathComponents[dirLength-5] + '_' + filename[:-4] + '_' + dateTime + '.mat'
				#print destIndividualFname
				if not os.path.isdir(destBaseDir): # let's make sure it doesn't exist already
					#print 'we make a dir'
					os.makedirs(destBaseDir)

				# if it exists we remove it - for completeness sake :)
				if os.path.isfile(destIndividualFname):
					#print 'File exists!'
					os.unlink(destIndividualFname)
				
				sourceMatFileName = dirpath + os.sep + filename
				print sourceMatFileName			
				#print 'Symlinking ' + filename
				os.symlink(sourceMatFileName,destIndividualFname)				
				
				
					
print 'Done!'						
					


