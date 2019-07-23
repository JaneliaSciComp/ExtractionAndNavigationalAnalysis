
# 20120219 - we'll skip analysis if it has already been run before :)
# For now we will only check if there's a matfiles directory in it

import os
import os.path
import shutil
import sys
import stat
import string
import re

sys.path.append('/groups/larvalolympiad/home/afonsob/BrunoAnalysis/settings/current')

import settings
import functions


# print checkerboardsFileNames['t7']
# print checkerboardsFileNames['t8']

# we decide if we create or not the mwt files from matlab
#extraLineParameters = ' createMWTFiles true'
extraLineParameters = ''


list_of_files = {}
path = "/groups/larvalolympiad/larvalolympiad/Extracted-files"
njob = 0 ;
for (dirpath, dirnames, filenames) in os.walk(path):
	for filename in filenames:
		if filename[-4:] == ".bin":
			os.path.normpath(filename)
			lineName = filename[:-16] 
			if os.path.isdir(dirpath + os.sep + 'matfiles'):
				print 'Skipping ' + lineName
			else:
				print '\r\n' + '------ ' + 'Processing ' + lineName + '------ '
				pathComponents = dirpath.split(os.sep)
				dirLength = len(pathComponents)
				tracker = pathComponents[dirLength-4]
				#print tracker
				lineHandle = str.split(lineName,'@')
				lineHandle = lineHandle[0] + '@' + lineHandle[1] + '@' + lineHandle[2] 
				lineHandle = string.replace(lineName,'#','_')
				lineHandle = string.replace(lineHandle,'@','_')
	
				shfile = settings.batchScriptDir + 'toMatFiles/' + lineHandle + '.sh'
	
				#print "Phototaxis Directional, going to process!"
				mcrCacheRoot = settings.mcrCacheRootBase  + lineHandle
				
				# we disabled the checkerboard
				expParameters = string.replace(pathComponents[6],'@','\@') + ' '
				expParameters = expParameters + extraLineParameters 
				
				functions.createQsubFile(shfile,settings.mcrLocation,settings.matlabScriptFileName[tracker] ,dirpath,expParameters) 
						
				
				pat = re.compile('t8')
				controlsPat = re.compile('FCF_|ywr')
				if pat.match(tracker) :
					qsubAdditional = ' -pe batch 16'
					#print 'we are matching tracker t8'
				else:
					qsubAdditional = ' -pe batch 3'
	
				#print qsubAdditional
				
				jobName = 'Mat_' + tracker + '_' + lineHandle[16:-3]  ;
				qsubOut = shfile[:-3] + '.log'
				njob = njob + 1;
				qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
	
				#print qsubCommand
				
	# 				# we copy the checkerboard
				#shutil.copy(settings.checkerboardsFileNames['t7'], dirpath)
				
				# we copy the camcalinfo file
				shutil.copy(settings.camcalinfo[tracker], dirpath + '/camcalinfo.mat')
				
				os.system(qsubCommand)				
				#sys.exit()

			
			
