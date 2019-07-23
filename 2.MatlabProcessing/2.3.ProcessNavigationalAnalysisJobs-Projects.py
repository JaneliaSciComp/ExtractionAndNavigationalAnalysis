import os
import os.path
import glob
import shutil
import sys
import string
import stat
import time
import filecmp
import re

sys.path.append('../settings')
import settings
import functions

def analyzeDirectory(tracker, directory, shellDir):
	# create the line handle from directory
	directoryComp = directory.split(os.sep)
	if 'individualMatfiles' in directoryComp:
		lineEffector = directoryComp[-4]
		expDateTime = directoryComp[-3]
		protocol = directoryComp[-1]
		lineName = "%s_%s_%s" % (lineEffector, expDateTime, protocol)
	else:
		lineEffector = directoryComp[-2]
		protocol = directoryComp[-1]
		lineName = "%s_%s" % (lineEffector, protocol)

	# if directoryComp[len(directoryComp)-2] == 'individualMatfiles':
	# 	lineName = directoryComp[len(directoryComp)-4] + '_' + directoryComp[len(directoryComp)-3] + '_' + directoryComp[len(directoryComp)-1]
	# else:
	# 	lineName = directoryComp[len(directoryComp)-2] + '_' + directoryComp[len(directoryComp)-1]

	cmdLineName = lineName
	normLineHandle = functions.sanitizeForFileName(lineName)
	normLineHandle = string.replace(normLineHandle,',','_')
	shfile = os.path.dirname(shellDir) + os.sep + settings.batchScriptDirProjectsSuffix + 'navigationalAnalysis/matlabNavAnalysis_' + tracker + '_' + normLineHandle + '.sh'
	expParameters = "'%s' 'runningOnCluster' '1' " % (cmdLineName)
	#functions.createQsubFile(shfile, settings.mcrLocation, settings.matlabScriptAnalysis[tracker], directory, expParameters)
	functions.createQsubFile(shfile, '/misc/local/matlab-2019a/', settings.matlabScriptAnalysis[tracker], directory, expParameters)
	qsubAdditional = ""
	
	if tracker == 't8':
		#qsubAdditional = ' -pe batch 3 '
		qsubAdditional = ' -n 3 '
	elif tracker == 't1':
		#qsubAdditional = ' -pe batch 1 '
		qsubAdditional = ' -n 1 '
	elif tracker in  settings.SPATIAL_TRACKERS:
		#qsubAdditional = ' -pe batch 1 '
		qsubAdditional = ' -n 1 '
	
	jobName = 'nav_' + tracker + '_' + normLineHandle ;
	qsubOut = shfile[:-3] + '.log'
	shfile = string.replace(shfile,',','_')
	jobName = string.replace(jobName,',','_')
	qsubAdditional += settings.supplementaryQsubParams[tracker]
	#qsubCommand = 'qsub -N ' + re.escape(jobName) + qsubAdditional + ' -j y -b y -o ' + re.escape(qsubOut) + ' -cwd ' + re.escape(shfile)
	qsubCommand = 'bsub -J ' + re.escape(jobName) + qsubAdditional + ' -o ' + re.escape(qsubOut) + ' ' + re.escape(shfile)
	os.system("chmod 755 " + re.escape(shfile))
	#qsubCommand = re.escape(shfile)
	functions.addQsubToQueue(qsubCommand)				
	return

projectsDirs = functions.getProjectDirs(settings.projectsPath)
for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		for (matFilesPath, matDirNames, matFileNames) in os.walk(fullProjectDirPath):
			pathComponents = matFilesPath.split(os.sep)
			tracker = functions.getTrackerName(pathComponents)
			if tracker in settings.rubenTrackers:
				continue
			for matDirName in matDirNames:
				if re.match('matfiles',matDirName): # we only process if we have a folder with .mat files
					# individual files are always closer to the end. First we check if it is an individual dir. If it's not, 
					# we see if an analysis file already exists or not. If so, do not run
					matFilesPathComp = matFilesPath.split(os.sep)
					possibleIndividualDir = matFilesPathComp[len(matFilesPathComp)-2]
					calcDir = matFilesPath + os.sep + 'calculations'
					# If it's an individual run and there's no calculations, just run it baby
					if re.match('individualMatfiles', possibleIndividualDir) and not os.path.isdir(calcDir) :
						tracker = functions.getTrackerName(matFilesPathComp)
						analyzeDirectory(tracker, matFilesPath, fullProjectDirPath)
					# else - a global analysis file - if there is not a calculations file, we don't run it, because we will combine it
					elif os.path.isdir(calcDir):
						analysisFilePresent = False
						# First we find if there is a an analysis file present previously combined
						analysisGlob = calcDir + os.sep + "*analysis.mat"
						if glob.glob(analysisGlob):
							analysisFilePresent = True
						figuresDir = matFilesPath + os.sep + "figures"
						figuresGlob = figuresDir + os.sep + "simpleMetrics*.pdf"
						figureFilePresent = False
						if glob.glob(figuresGlob):
							figureFilePresent = True
						# If there's not figure but analysis is present, we run 
						if (not figureFilePresent and analysisFilePresent):

							tracker = functions.getTrackerName(matFilesPathComp)
							analyzeDirectory(tracker, matFilesPath, fullProjectDirPath)	
functions.runAllQsubsToCompletion()
