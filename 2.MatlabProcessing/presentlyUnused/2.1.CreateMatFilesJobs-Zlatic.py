# 20130326
# I'm converting Marta's mwt stuff into out matlab analysis. This is not really an extraction, it's simply how to initially get them to be .mat files

import os
import os.path
import shutil
import sys
import stat
import string

sys.path.append('/groups/larvalolympiad/home/afonsob/BrunoAnalysis/settings/current')

import settings
import functions
import re
#import functions


# print checkerboardsFileNames['t7']
# print checkerboardsFileNames['t8']

# we decide if we create or not the mwt files from matlab
#extraLineParameters = ' createMWTFiles true'
extraLineParameters = ''


list_of_files = {}
# disabled
# path = '/groups/zlatic/zlaticlab/pipeline/screen/tracking-results/t1'

projectsDirs = functions.getProjectDirs(settings.zlaticProjectsPath)

for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		print fullProjectDirPath
		#sys.exit()
		#fullProjectDirPath = projectsPath + os.sep + dir
		#print fullProjectDirPath
		
		path = fullProjectDirPath #+ os.sep + "Extracted-files" 
		#print path		
		
	njob = 0 ;

	for (dirpath, dirnames, filenames) in os.walk(path):
		for filename in filenames:
			
			#print dirpath
			if filename[-8:] == ".summary":
				
				# There is a "rob" subfolder we must skip
				if re.match('.*\/rob\/*',dirpath):
					print "we skip 'rob' subfolder"
					break

				os.path.normpath(filename)
				lineName = filename[:-16] 
				fname,ext= os.path.splitext(filename)
				# let's extract the line name with effectors, etc on it :-)
				m = re.search('(\S+?)#\S*',fname)
				#print m.group(0)
				lineName =  m.group(1)

				#print lineName
				#break
				# print filename
				# print lineName
				
				if os.path.isdir(dirpath + os.sep + 'matfiles'):
					print 'Skipping ' + lineName
				else:
					print '\r\n' + '------ ' + 'Processing ' + lineName + '------ '
					
					pathComponents = dirpath.split(os.sep)
					dirLength = len(pathComponents)
					tracker = pathComponents[dirLength-4]
					#
					# print pathComponents
					# print tracker
					# # break
					lineHandle = str.split(lineName,'@')
					lineHandle = lineHandle[0] + '@' + lineHandle[1] + '@' + lineHandle[2] 
					lineHandle = string.replace(lineName,'#','_')
					lineHandle = string.replace(lineHandle,'@','_')
					
					#print lineHandle

					shfile = settings.batchScriptDirZlatic + 'toMatFiles/' + lineHandle + '.sh'

					#print "Phototaxis Directional, going to process!"
					mcrCacheRoot = settings.mcrCacheRootBase  + lineHandle
					
					expParameters =  '_'.join(pathComponents[len(pathComponents)-3:len(pathComponents)-1])
					
					#expParameters = string.replace(expParameters,'@','\@') + ' '
					expParameters = expParameters + extraLineParameters 

					#mcrLocation = '/usr/local/matlab-2012b/'
					functions.createQsubFile(shfile,settings.mcrLocation,settings.matlabScriptFileName[tracker] ,dirpath,expParameters) 
					
					#print shfile

					
					# pat = re.compile('t8')
					# controlsPat = re.compile('FCF_|ywr')
					# if pat.match(tracker) :
					# 	qsubAdditional = ' -pe batch 8 -l mem96=true'
					# 	#print 'we are matching tracker t8'
					# else:
					
					qsubAdditional = ' -pe batch 1 -l new '
		
					#print qsubAdditional
					
					# For the time being, we are using always the top dogs !
					# qsubAdditional = ' -pe batch 8 -l mem96=true'

					jobName = 'Mat_' + tracker + '_' + lineHandle[16:-3]  ;
					#print jobName
					
					qsubOut = shfile[:-3] + '.log'
					njob = njob + 1;
					qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
		
					#print qsubCommand
					
		# 				# we copy the checkerboard
					#shutil.copy(settings.checkerboardsFileNames['t7'], dirpath)
					
					# we copy the camcalinfo file
					#shutil.copy(settings.camcalinfo[tracker], dirpath + '/camcalinfo.mat')
					
					os.system(qsubCommand)				
					#sys.exit()

			
			
