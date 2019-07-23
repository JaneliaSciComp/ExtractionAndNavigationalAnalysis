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

# let's get a list of directories in Projects
projectsDirs = functions.getProjectDirs(settings.projectsPath)
for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		path = fullProjectDirPath + os.sep + "Extracted-files" 
		njob = 0
		##GO THROUGH EXTRACTED FILES
		for (dirpath, dirnames, filenames) in os.walk(path):
			sumBinFileSizes = 0
			pathComponents = dirpath.split(os.sep)
			# we find where the "Extracted-files" folder is and then assume the tracker is on the next subdir structure. Not super robust..
			tracker = functions.getTrackerName(pathComponents)
			if tracker in settings.rubenTrackers:
				##IGNORE NON T16 TRACKERS
				for filename in filenames:
					##CHECK IF WE NEED TO RUN NEW DATA
					if (filename[-4:] == ".bin" and
						not filename.endswith('values.bin') and
						not filename.endswith('led1.bin') and
						not filename.endswith('led2.bin')) : # we only care about bin files
						
						btdfile = 'btdfiles/btd_' + filename[:-4] + ".mat"
						os.path.normpath(filename)
						lineName, filenameExtension = os.path.splitext(filename)
						if os.path.isfile(dirpath + os.sep + btdfile):
							print 'Skipping ' + lineName
						else:
							#run that line
							print 'Running ' + lineName
							lineHandle = functions.sanitizeForFileName(lineName)
							shfile = os.path.dirname(fullProjectDirPath) + os.sep + settings.batchScriptDirProjectsSuffix + 'totalAnalysis/' + lineHandle + '.sh'
							#scratch location
							mcrCacheRoot = settings.mcrCacheRootBase  + lineHandle
							expParameters = lineName
							functions.createQsubFile(shfile, settings.mcrLocation, settings.matlabScriptComplete[tracker], dirpath, None) 
							#qsubAdditional = ' -pe batch 8 -l h_rt=2:00:00' + settings.supplementaryQsubParams[tracker]
							qsubAdditional = ' -n 8 -W 120' + settings.supplementaryQsubParams[tracker]
							jobName = 'Mat_' + tracker + '_' + lineHandle[16:-3]  ;
							qsubOut = shfile[:-3] + '.log'
							njob = njob + 1;
							#qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
							qsubCommand = 'bsub -J ' + jobName + qsubAdditional + ' -o ' + qsubOut + ' ' + shfile
							os.system("chmod 755 " + shfile)
							#qsubCommand = shfile
							functions.addQsubToQueue(qsubCommand)				
functions.runAllQsubsToCompletion()
			
