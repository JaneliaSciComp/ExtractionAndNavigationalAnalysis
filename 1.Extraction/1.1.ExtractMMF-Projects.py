# trying python..
# skipping directories already extracted!
# 20120611 - we limit how long the run can be
# 20120629 - need to limit this to our trackers of interest(!) - no t12 stuff !

import os
import os.path
import shutil
import sys
import stat
import string
import time
import datetime 
import re

sys.path.append('../settings/')
import settings
import functions

projectsDirs = functions.getProjectDirs(settings.projectsPath)

for fullProjectDirPath in projectsDirs:
	print "Full ProjectDirPath", fullProjectDirPath
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		njob = 0 ;
		for (dirpath, dirnames, filenames) in os.walk(fullProjectDirPath):
			for filename in filenames:
				if filename[-4:] == ".mmf":
					print "MMF file", filename
					# by default we extract the line..
					runLine = True;
					rightTracker = False;
					# we're going to define the directory
					pathComponents = dirpath.split(os.sep)
					tracker = functions.getTrackerName(pathComponents)
					# make sure we are dealing with a tracker we want to. Likely want to move to settings
					if tracker in settings.mmfTrackers:
						rightTracker = True
					else:
						continue
					extractionOptions = settings.extractionOptions[tracker]					
					# let's build the final extraction directory
					extractionDir = fullProjectDirPath +  os.sep + 'Extracted-files'
					extractionDir += os.sep + functions.secondaryDataSuffix(pathComponents, tracker)
					lineName = filename.split('@')
					lineName = filename[:-4]
					# DO I NEED TO RUN IT OR NOT PART
					if os.path.isdir(extractionDir): #we may need to re-run this line, extraction may have failed...
						# let's make sure there is not a bin file there.
						for (extdirpath, extdirnames, extfilenames) in os.walk(extractionDir):
							for extfname in extfilenames:
								#TODO check for actual output name because there will be more than 1 bin file for t16
								if extfname[-4:] == ".bin":
									runLine = False
					if (not os.path.isdir(extractionDir) or runLine) and rightTracker:
						mmfFile = dirpath + os.sep + filename 
						pathComponents = dirpath.split(os.sep)
						dirLength = len(pathComponents)
						lineHandle = functions.sanitizeForFileName(lineName)
						batchScriptDir = os.path.dirname(fullProjectDirPath) + os.sep + settings.batchScriptDirProjectsSuffix + os.sep + 'extraction'
						if not os.path.exists(batchScriptDir):
							os.makedirs(batchScriptDir)
						shfile = batchScriptDir + '/' + lineHandle + '_' + tracker + '.sh'
						if not os.path.isdir(extractionDir):
							os.makedirs(extractionDir)

						shfile = batchScriptDir + '/' + lineHandle + '_' + tracker + '.sh'
						extractFile = extractionDir + os.sep + lineHandle + '.bxx'
						functions.createExtractFile(extractFile, mmfFile, extractionDir, extractionOptions)
						functions.createQsubExtractFile(shfile, extractFile, settings.settingsDir, os.path.dirname(mmfFile))
						jobName = 'ext' + lineHandle + '_' + str(njob) ;
						qsubOut = shfile[:-3] + '.log'
						#qsubCommand = 'qsub -l short -N ' + settings.supplementaryQsubParams[tracker] +  'ext_' + string.replace(lineName[:11],'@','_') + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
						qsubCommand = 'bsub -J ' + settings.supplementaryQsubParams[tracker] +  'ext_' + string.replace(lineName[:11],'@','_') + ' -o ' + qsubOut + ' ' + shfile
						os.system("chmod 755 " + shfile)
						#qsubCommand = shfile						
						njob = njob + 1
						functions.addQsubToQueue(qsubCommand)
functions.runAllQsubsToCompletion()
