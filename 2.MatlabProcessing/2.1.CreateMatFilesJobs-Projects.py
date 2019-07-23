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
		for (dirpath, dirnames, filenames) in os.walk(path):
			sumBinFileSizes = 0
			pathComponents = dirpath.split(os.sep)
			tracker = functions.getTrackerName(pathComponents)
			if tracker in settings.rubenTrackers:
				continue
			for filename in filenames:
				if filename[-4:] == ".bin" : # we only care about bin files
					# we manually add this so that bad bins don't re run ad eternum. These should be deleted
					badPathName = dirpath + os.sep + "bad"
					# this exists if the mmf -> bin extractor ran into problems before
					badFileName = dirpath + os.sep + filename[:-4] + os.extsep + "bad" 
					mdatFileName = dirpath + os.sep + filename[:-4] + os.extsep + "mdat"
					if not (os.path.isfile(badFileName) or os.path.isdir(badPathName) or not os.path.isfile(mdatFileName) ) : # we skip if the extraction is bad
						#there is a bin but it is bad
						os.path.normpath(filename)
						lineName, filenameExtension = os.path.splitext(filename)
						if os.path.isdir(dirpath + os.sep + 'matfiles'):
							print 'Skipping ' + lineName
						else:
							print '\r\n' + '------ ' + 'Processing ' + lineName + '------ '
							pathComponents = dirpath.split(os.sep)
							dirLength = len(pathComponents)
							# we find where the "Extracted-files" folder is and then assume the tracker is on the next subdir structure. Not super robust..
							tracker = functions.getTrackerName(pathComponents)
							lineHandle = functions.sanitizeForFileName(lineName)
							shfile = os.path.dirname(fullProjectDirPath) + os.sep + settings.batchScriptDirProjectsSuffix + 'toMatFiles/' + lineHandle + '.sh'
							mcrCacheRoot = settings.mcrCacheRootBase  + lineHandle
							expParameters = lineName
							
							functions.createQsubFile(shfile,settings.mcrLocation,settings.matlabScriptFileName[tracker] ,dirpath,expParameters) 
							if (os.path.exists(dirpath+os.sep+filename)):
								sumBinFileSizes += os.path.getsize(dirpath+os.sep+filename)
							numBatchSlots = max(2,min(16,int(sumBinFileSizes*1e-9)))
							controlsPat = re.compile('FCF_|ywr')
							if tracker == 't8' :
								#qsubAdditional = ' -pe batch 16'
								qsubAdditional = ' -n 16'
							else:
								#qsubAdditional = ' -pe batch ' + str(numBatchSlots)
								qsubAdditional = ' -n ' + str(numBatchSlots)
							#qsubAdditional = qsubAdditional + ' -l h_rt=2:00:00' + settings.supplementaryQsubParams[tracker]
							qsubAdditional = qsubAdditional + ' -W 120' + settings.supplementaryQsubParams[tracker]
							jobName = 'Mat_' + tracker + '_' + lineHandle[16:-3]  ;
							qsubOut = shfile[:-3] + '.log'
							njob = njob + 1;
							#qsubCommand = 'qsub -N ' + jobName + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
							qsubCommand = 'bsub -J ' + jobName + qsubAdditional + ' -o ' + qsubOut + ' ' + shfile
							os.system("chmod 755 " + shfile)
							#qsubCommand = shfile
							print "Preparing to copy " + settings.camcalinfo[tracker] + " TO " + dirpath + '/camcalinfo.mat\n'
							shutil.copyfile(settings.camcalinfo[tracker], dirpath + '/camcalinfo.mat')
							functions.addQsubToQueue(qsubCommand)				
functions.runAllQsubsToCompletion()
			
