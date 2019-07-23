import os
import os.path
import shutil
import sys
import stat
import string
import re

sys.path.append('../settings')
import settings
import functions

extraLineParameters = ''
list_of_files = {}
projectsDirs = functions.getProjectDirs(settings.zlaticProjectsPath)
print projectsDirs
print settings.zlaticProjectsPath
for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		path = fullProjectDirPath #+ os.sep + "Extracted-files" 		
	njob = 0 ;
	batchDirectory = settings.batchScriptDirZlatic + 'toMatFiles/'
	if not os.path.isdir(batchDirectory):
		os.makedirs(batchDirectory)
	for (dirpath, dirnames, filenames) in os.walk(path):
		pathComponents = dirpath.split(os.sep)
		tracker = functions.getTrackerName(pathComponents)
		if tracker in settings.rubenTrackers:
			continue
		for filename in filenames:
			if filename[-8:] == ".summary":
				if re.match('.*\/rob\/*',dirpath):
					print "we skip 'rob' subfolder"
					break
				os.path.normpath(filename)
				lineName = filename[:-16] 
				fname, ext= os.path.splitext(filename)
				m = re.search('(\S+?)#\S*',fname)
				lineName =  m.group(1)
				if os.path.isdir(dirpath + os.sep + 'matfiles'):
					# print 'Skipping ' + lineName
					pass
				else:
					print '\r\n' + '------ ' + 'Processing ' + lineName + '------ '
					pathComponents = dirpath.split(os.sep)
					dirLength = len(pathComponents)
					tracker = pathComponents[dirLength-4]
					lineHandle = lineName.split('@')
					lineHandle = lineHandle[0] + '@' + lineHandle[1] + '@' + lineHandle[2] 
					lineHandle = string.replace(lineName,'#','_')
					lineHandle = string.replace(lineHandle,'@','_')
					shfile = settings.batchScriptDirZlatic + 'toMatFiles/' + lineHandle + '.sh'
					#print "Phototaxis Directional, going to process!"
					mcrCacheRoot = settings.mcrCacheRootBase  + lineHandle
					expParameters =  '_'.join(pathComponents[len(pathComponents)-3:len(pathComponents)-1])
					expParameters = expParameters + extraLineParameters
					functions.createQsubFile(shfile, settings.mcrLocation, settings.matlabScriptFileName[tracker], dirpath, expParameters) 
					#qsubAdditional = ' -pe batch 1 ' + settings.supplementaryQsubParams[tracker]
					qsubAdditional = ' -n 1 ' + settings.supplementaryQsubParams[tracker]
					jobName = 'Mat_' + tracker + '_' + lineHandle[16:-3]  ;
					qsubOut = shfile[:-3] + '.log'
					njob = njob + 1;
					#qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile					
					qsubCommand = 'bsub -J ' + jobName + qsubAdditional + ' -o ' + qsubOut + ' ' + shfile
					os.system("chmod 755 " + shfile)
					#qsubCommand = shfile
					functions.addQsubToQueue(qsubCommand)
functions.runAllQsubsToCompletion()

