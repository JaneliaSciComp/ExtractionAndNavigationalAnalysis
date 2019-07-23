import settings
import os
import datetime
import re
import shutil
import string
import sys
#import yaml

qsubQueue = []

def sanitizeForFileName(textToSanitize):
	textToSanitize = string.replace(textToSanitize,'#','_')
	textToSanitize = string.replace(textToSanitize,'@','_')
	sanitizedText = string.replace(textToSanitize,' ','_')
	return sanitizedText

# we create a file this way :)
def createQsubFile(shfile, mcrLocation, script, expDir, expParameters):
	expDir = os.path.normpath(expDir)
	f = open(shfile, 'w')
	f.write('#!/bin/bash \n')
	f.write('\n')
	f.write('# This script will be qsubbed\n')
	from time import gmtime, strftime
	mcrCacheRoot = settings.mcrCacheRootBase + 'matlabCache' ;
	#f.write('export MCR_CACHE_ROOT=' + mcrCacheRoot + '.$JOB_ID \n\n')
	f.write('export MCR_CACHE_ROOT=' + mcrCacheRoot + '.$LSB_BATCH_JID \n\n')
	f.write('echo `date` \n\n')
	f.write('echo $MCR_CACHE_ROOT \n\n')
	f.write('export MCR_INHIBIT_CTF_LOCK=1\n')
	f.write('umask 002\n')
	if expParameters:
		f.write("%s %s '%s/' %s\n" % (script, mcrLocation, expDir, expParameters))
	else:
		f.write("%s %s '%s/'\n" % (script, mcrLocation, expDir))  
	f.write('rm -rf $MCR_CACHE_ROOT \n')
	f.close 
	try:
		os.chmod(shfile,0744)
	except Exception, e:
		print "Error chmodding %s" % (shfile)	
	return
	
	
# we create a file this way :)
def createQsubExtractFileIterations(shfile, extractionFile, settingsDir, mmfDir, extractDir, supDataDir, camcalFile, iterations=None):
	f = open(shfile, 'w')
	f.write('#!/bin/bash \n')
	f.write('\n')
	f.write('export LD_LIBRARY_PATH="/misc/local/OpenCV-1.0.0/lib/" \n')
	f.write('echo $LD_LIBRARY_PATH \n')
	f.write('# This script will be qsubbed\n')
	f.write('cp ' +  camcalFile + ' ' + extractDir + os.sep + "camcalinfo.mat\n")
	f.write('OIFS="$IFS"\n')
	f.write("IFS=$'\\n'\n")
	#TODO copy camcal info for t16 to camcalinfo.mat
	if not iterations:
		f.write(settingsDir + os.sep + 'extract-stack.exe "' + extractionFile + '"\n')
		#copy if less than 5MB
		f.write('for f in `find "' + mmfDir + '" -type f -size -5M`\n')
		f.write('do\n')
		f.write('    filename=`basename $f`\n')
		f.write('    mkdir -p "' + extractDir + os.sep + supDataDir + ' sup data dir' + os.sep +'"\n')
		f.write('    cp "$f" "' + extractDir + os.sep + supDataDir + ' sup data dir' + os.sep +'"\n')
		f.write('done\n')
	else:
		for i in range(iterations):
			f.write(settingsDir + os.sep + 'extract-stack.exe "' + extractionFile + "-" + str(i) + '.bxx' + '"\n')
		f.write('for f in `find "' + mmfDir + '" -type f -size -5M`\n')
		f.write('do\n')
		for i in range(iterations):
			#copy if less than 5MB
			f.write('    mkdir -p "' + extractDir + os.sep + supDataDir + "-" + str(i) + ' sup data dir' + os.sep +'"\n')
			f.write('    cp "$f" "' + extractDir + os.sep + supDataDir + "-" + str(i) + ' sup data dir' + os.sep +'"\n')
		f.write('done\n')	
	f.close()
	try:
		os.chmod(shfile,0777)
	except:
		print "bad shell file ", shfile
	return

def createQsubExtractFile(shfile, extractionFile, settingsDir, mmfDir):
	f = open(shfile, 'w')
	f.write('#!/bin/bash \n')
	f.write('\n')
	f.write('export LD_LIBRARY_PATH="/misc/local/OpenCV-1.0.0/lib/" \n')
	f.write('echo $LD_LIBRARY_PATH \n')
	f.write('# This script will be qsubbed\n')
	#TODO copy camcal info for t16 to camcalinfo.mat

	f.write(settingsDir + os.sep + 'extract-stack.exe "' + extractionFile + '"\n')
	f.close()
	try:
		os.chmod(shfile,0777)
	except:
		print "bad shell file ", shfile
	return

#def createExtractFileYaml(extractFile, mmfFile, destinationDir, extractionOptions, iteration=None):
#	batch = yaml.load('defaultBatchFile.bxx')
#	mmfFname = os.path.basename(mmfFile)
#	mmfName, mmfExtension = os.path.splitext(mmfFname)
#	mmfDirName = os.path.dirname(mmfFile)
#	today = datetime.datetime.today()
#	iteration_suffix = ""
#	for option in extractionOptions.keys():
#		batch['processing params'][option] = extractionOptions[option]
#	if iteration is not None:
#		iteration_suffix = "-" + str(iteration)
#		batch['processing params']['startFrame'] = extractionOptions['startFrame'] + (iteration * extractionOptions['maxFrames'])
#		batch['processing params']['endFrame'] = min(extractionOptions['endFrame'], (extractionOptions['startFrame'] + ((iteration + 1) * extractionOptions['maxFrames'])))
#	batch['file stub'] = mmfDirName + os.sep + mmfName
#	batch['output file'] = destinationDir + os.sep + mmfName + iteration_suffix 
#	batch['fstub'] = mmfDirName + os.sep + mmfName 
#	batch['extension'] = mmfFname.split('.')[1]
#	batch['outputname'] = destinationDir + os.sep + mmfName + iteration_suffix + '.bin'
#	batch['headerinfoname'] = destinationDir + os.sep + mmfName + iteration_suffix + '_header.txt'
#	batch['logName'] = destinationDir + os.sep + mmfName + '_' + iteration_suffix + today.strftime("%Y%m%d_%H%M%S") + '_log.txt'
#	
#	f = open(extractFile, 'w')
#	f.write(yaml.dumps(batch))
#	f.close()
#	os.chmod(extractFile, 0744)
	
def createExtractFile(extractFile, mmfFile, destinationDir, extractionOptions, iteration=None):
	
	mmfFname = os.path.basename(mmfFile)
	mmfName, mmfExtension = os.path.splitext(mmfFname)
	mmfDirName = os.path.dirname(mmfFile)
	today = datetime.datetime.today()
	iteration_suffix = ""
	if iteration is not None:
		iteration_suffix = "-" + str(iteration)

	f = open(extractFile, 'w')
	f.write('files to process:\r\n')
	f.write('  - file stub: ' + mmfDirName + os.sep + mmfName + '\r\n')
	f.write('    output file: ' + destinationDir + os.sep + mmfName + iteration_suffix + '.bin' + '\r\n')
	f.write('    processing params:\r\n')
	f.write('      fstub: ' + mmfDirName + os.sep + mmfName + '\r\n')
	f.write('      extension: mmf\r\n')
	f.write('      padding: ' + str(extractionOptions['padding']) + '\r\n')
	f.write('      outputname: ' + destinationDir + os.sep + mmfName + iteration_suffix + '.bin' + '\r\n')
	f.write('      headerinfoname: ' + destinationDir + os.sep + mmfName + iteration_suffix + '_header.txt' + '\r\n')
	f.write('      logName: ' + destinationDir + os.sep + mmfName + '_' + iteration_suffix + today.strftime("%Y%m%d_%H%M%S") + '_log.txt' + '\r\n')
	f.write('      verbosity level: ' + str(extractionOptions['verbosityLevel']) + '\r\n')
	if iteration is not None:
		f.write('      startFrame: ' + str(extractionOptions['startFrame'] + (iteration * extractionOptions['maxFrames']))  + '\r\n')
		endFrame = min(extractionOptions['endFrame'], (extractionOptions['startFrame'] + ((iteration + 1) * extractionOptions['maxFrames'])))
		f.write('      endFrame: ' + str(endFrame) + '\r\n')
	else:
		f.write('      startFrame: ' + str(extractionOptions['startFrame']) + '\r\n')
		f.write('      endFrame: ' + str(extractionOptions['endFrame']) + '\r\n')
	f.write('      analysis rectangle:\r\n' )
	f.write('        - ' + str(extractionOptions['analysisRectangle'][0]) + '\r\n')
	f.write('        - ' + str(extractionOptions['analysisRectangle'][1]) + '\r\n')
	f.write('        - ' + str(extractionOptions['analysisRectangle'][2]) + '\r\n')
	f.write('        - ' + str(extractionOptions['analysisRectangle'][3]) + '\r\n')
	f.write('      minArea: ' + str(extractionOptions['minArea']) + '\r\n')
	f.write('      maxArea: ' + str(extractionOptions['maxArea']) + '\r\n')
	f.write('      overallThreshold: ' + str(extractionOptions['overallThreshold']) + '\r\n')
	f.write('      winSize: ' + str(extractionOptions['winSize']) + '\r\n')
	f.write('      nBackgroundFrames: ' + str(extractionOptions['nBackgroundFrames']) + '\r\n')
	f.write('      background_resampleInterval: ' + str(extractionOptions['background_resampleInterval']) + '\r\n')
	f.write('      background_blur_sigma: ' + str(extractionOptions['background_blur_sigma']) + '\r\n')
	f.write('      thresholdScaleImage: ' + str(extractionOptions['thresholdScaleImage']) + '\r\n')
	f.write('      blurThresholdIm_sigma: ' + str(extractionOptions['blurThresholdIm_sigma']) + '\r\n')
	f.write('      frame normalization method: ' + str(extractionOptions['frameNormalizationMethod']) + '\r\n')
	f.write('      imStackLength: ' + str(extractionOptions['imStackLength']) + '\r\n')
	f.write('      maxExtractDist: ' + str(extractionOptions['maxExtractDist']) + '\r\n')
	f.write('      showExtraction: ' + str(extractionOptions['showExtraction']) + '\r\n')
	f.write('      max maggot contour angle: ' +str(extractionOptions['maxMaggotContourAngle']) + '\r\n')
	f.write('default processing params: ~')
	f.close
	try:
		os.chmod(extractFile,0744)
	except:
		print "bad extract file ", extractFile
	return

def getProjectDirs(projectsPath):
	projectsDirs = [] ;
	for d in projectsPath:
		thisProjectsDirs = os.listdir(d)
		for projDir in thisProjectsDirs:
			projectsDirs.append(d + os.sep + projDir)

	return projectsDirs


def md5_for_file(filename, blockMultiplier):
	import hashlib
	md5 = hashlib.md5()
	while True:
		f = open(filename,'rb')
		data = f.read(blockMultiplier*md5.block_size)
		if not data:
			break
		md5.update(chunk)
	return md5.digest()

def findIndexOfExtractedFiles(pathComponents):
	# we find where the "Extracted-files" folder is and then assume the tracker is on the next subdir structure. Not super robust..
	i = 0	
	for comp in pathComponents:
		if not re.match('Extracted-files',comp):
			i=i+1
		else:
			break
	return i

# here we will match either Mat-Files or Extracted-Files in order to find the tracker
def findTrackerFromPath(pathComponents):
	i = 0
	a = False
	for comp in pathComponents:
		if re.match('Extracted-files|Mat-files',comp, flags=re.IGNORECASE):
			a = i 
			return a
		if re.match('MMF-Files',comp, flags=re.IGNORECASE):
			a = i
			return a
		i = i + 1	
	return a

def getTrackerName(pathComponents):
	for c in pathComponents:
		if re.match("^t\d+$", c):
			return c
	return False

def secondaryDataSuffix(pathComponents, tracker):
	suffix = ""
	try:
		tracker_index = pathComponents.index(tracker)
		return os.sep.join(pathComponents[tracker_index:])
	except:
		return False
		

# here we will match either Mat-Files or Extracted-Files in order to find the tracker
def findTrackingResultsFromPath(pathComponents):
	i = 0
	a = 0
	# print pathComponents
	for comp in pathComponents:
		# if re.match('Extracted-Files|Mat-files',comp):
		if re.match('tracking-results',comp):
			a = i 
			return a
		i = i + 1	
	return a

# this function returns a variable mustRun that tells you if we must or not run the calculations. We must run if files symliked differ from the ones on the list 
def checkCombMatfileList(matFilesPath):
	mustRun = False
	matfilesFullPath =  matFilesPath + os.sep + 'matfiles'
	calculationsFullPath =  matFilesPath + os.sep + 'calculations'
	combineFilesFname = calculationsFullPath + os.sep + 'combinedFiles.txt'

	fileLines =  []
	if os.path.isfile(combineFilesFname):
		text = open(combineFilesFname,'r')
		for line in text:
			fileLines.append(line)
	else:
		mustRun = True
		return mustRun
	text.close()
	for (matPath, matDir, matSymlinkedFiles) in os.walk(matfilesFullPath):
		if len(fileLines) == len(matSymlinkedFiles):
			fi = 0
			for matSymlinkedFile in matSymlinkedFiles:
				if not fileLines[fi].find(re.escape(matSymlinkedFile)):
					mustRun = True
					return mustRun
				fi = fi + 1

			mustRun = False
			return mustRun
		else:
			mustRun = True
			return mustRun

def deleteFiguresPath(basePath):
	figuresFullPath = basePath + os.sep + 'figures'
	print "Deleting ", figuresFullPath
	try:
		shutil.rmtree(figuresFullPath)
	except:
		print "Error deleteing", figuresFullPath

def writeCombMatfileList(matFilesPath):
	# return
	matfilesFullPath =  matFilesPath + os.sep + 'matfiles'
	calculationsFullPath =  matFilesPath + os.sep + 'calculations'
	combineFilesFname = calculationsFullPath + os.sep + 'combinedFiles.txt'
	if not os.path.isdir(calculationsFullPath):
		os.makedirs(calculationsFullPath)
	f = open(combineFilesFname,'w')
	for (matPath, matDir, matSymlinkedFiles) in os.walk(matfilesFullPath):
		for matSymlinkedFile in matSymlinkedFiles:
			if re.match('\S+\.mat',matSymlinkedFile):
				# print matSymlinkedFile
				f.write(matSymlinkedFile + '\n')
	f.close()



def addQsubToQueue(qsubString):
	qsubQueue.append(qsubString)
	
def runAllQsubsToCompletion():
	# create a suitable uniquely-named temp file here
	#
	# open that file and
	avoidDups = {}

	if qsubQueue:
		qfile = settings.mainProjectsPath + "/bsubList." + str(os.getpid()) + ".sh"
		f = open(qfile,'w')
		#TODO use SET?
		for job in qsubQueue:
			if job not in avoidDups:
				avoidDups[job] = 1
				f.write(job)
				f.write("\n")
		f.close()
		# submit bsubfiles
		print "QFILE: " + qfile
		os.chmod(qfile,0777)
		os.system(qfile)
		#os.system(settings.sgeSyncPath + " --file " + qfile)
		#os.unlink(qfile)


def CombineCalculationsinDirectory(tracker, directory, projectDir):
	# create the line handle from directory
	directoryComp = directory.split(os.sep)
	if directoryComp[len(directoryComp)-2] == 'individualMatfiles':
		sys.exit() # we should NEVER see this
		lineName = directoryComp[len(directoryComp)-4] + '_' + directoryComp[len(directoryComp)-1]
	else:
		i = findTrackerFromPath(directoryComp)
		# print directoryComp[i]
		tracker = directoryComp[i+1]
		# old way
		lineName = directoryComp[len(directoryComp)-2]
		# new way
		lineName = directoryComp[i+2]
		experimentalConditions = directoryComp[i+3]

	sanitizedLineName=sanitizeForFileName(lineName)
	sanitizedExperimentalConditions = sanitizeForFileName(experimentalConditions)
	runInformation = sanitizedLineName + '_' + sanitizedExperimentalConditions 
	
	# Create the .sh file
	shfile = os.path.dirname(projectDir) + settings.batchScriptDirProjectsSuffix + 'CombineCalculations/CombineCalcs_' + tracker + '_' + runInformation + '.sh'
	shfile = string.replace(shfile,' ','_')
	shfile = string.replace(shfile,',','_')
	# Combine calculations required no parameters at all
	expParameters = '';
	
	# Let's rename figures if we have them
	if os.path.isdir(directory):
		simpleFig = directory + os.sep + 'figures' + os.sep + 'simpleMetrics.pdf'
		# print simpleFig
		if os.path.isfile(simpleFig):
			today = datetime.date.today()
			renamedSimpleFig = simpleFig[:-4] + '_' + today.strftime('%Y%m%d') + '.pdf'
			# print renamedSimpleFig
			os.rename(simpleFig,renamedSimpleFig)
		simpleFig = directory + os.sep + 'figures' + os.sep + 'temporalDetail.pdf'
		if os.path.isfile(simpleFig):
			today = datetime.date.today()
			renamedSimpleFig = simpleFig[:-4] + '_' + today.strftime('%Y%m%d') + '.pdf'
			os.rename(simpleFig,renamedSimpleFig)
		simpleFig = directory + os.sep + 'figures' + os.sep + 'strategyMetrics.pdf'
		if os.path.isfile(simpleFig):
			today = datetime.date.today()
			renamedSimpleFig = simpleFig[:-4] + '_' + today.strftime('%Y%m%d') + '.pdf'
			os.rename(simpleFig,renamedSimpleFig)

	pat = re.compile('t1|t7|t9|t10|t8|t14')
	controlsPat = re.compile('FCF_|ywr')
	if pat.match(tracker) :
		#createQsubFile(shfile,settings.mcrLocation,settings.combineCalcs[tracker],directory,expParameters)
		createQsubFile(shfile,'/misc/local/matlab-2019a/',settings.combineCalcs[tracker],directory,expParameters)
		#qsubAdditional = ' -pe batch 1'
		qsubAdditional = ' -n 1'
		if controlsPat.match(lineName[:4]):
			#qsubAdditional = ' -pe batch 5'
			qsubAdditional = ' -n 5'
	else:
		print 'tracker does not match!'
		return
	
	if re.search(tracker,'t8'):
		jobName = 'combTCalc_' + tracker + '_' + runInformation ;
	else:		
		jobName = 'combSCalc_' + tracker + '_' + runInformation ;
	
	qsubOut = shfile[:-3] + '.log'
	#qsubCommand = "qsub -N '" + jobName + "'" + settings.supplementaryQsubParams[tracker] + qsubAdditional + ' -j y -b y -o ' + qsubOut + ' -cwd ' + shfile
	qsubCommand = "bsub -J '" + jobName + "'" + settings.supplementaryQsubParams[tracker] + qsubAdditional + ' -o ' + qsubOut + ' ' + shfile
	os.system("chmod 755 " + shfile)
	#qsubCommand = shfile
	addQsubToQueue(qsubCommand)
	return
