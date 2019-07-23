# 20121114 - Combining calculations here

import os
import os.path
import shutil
import sys
import stat
import string
import filecmp
import re
import datetime

sys.path.append('../settings')
import settings
import functions

projectsDirs = functions.getProjectDirs(settings.projectsPath)
for fullProjectDirPath in projectsDirs:
	if not settings.ignoreDirPat.match(fullProjectDirPath) :
		matfileProjectDirPath = fullProjectDirPath + os.sep + 'Mat-files'
		for (matFilesPath, matDirNames, matFileNames) in os.walk(matfileProjectDirPath):
			pathComponents = matFilesPath.split(os.sep)
			tracker = functions.getTrackerName(pathComponents)
			if tracker in settings.rubenTrackers:
				continue
			for matDirName in matDirNames:
				if re.match(matDirName,'matfiles'): # we only process if we have a folder with .mat files - Even though we don't care about them here
					calculationsFullPath =  matFilesPath + os.sep + 'calculations'
					matFilesPathComp = matFilesPath.split(os.sep)
					tracker = functions.getTrackerName(matFilesPathComp)
					possibleIndividualDir = matFilesPathComp[len(matFilesPathComp)-2]
					# By default we don't run the combination of analysis..
					mustRun = False
					individualAnalysisFilesPresent = False
					individualMatFilesDir =  matFilesPath + os.sep + 'individualMatfiles'
					if not re.search(possibleIndividualDir, 'individualMatfiles'):
						for (calcPath, calcDir, calcFnames) in os.walk(individualMatFilesDir):
							for calcFname in calcFnames:
								if re.match('.*analysis\.mat',calcFname):
									individualAnalysisFilesPresent = True
						if not individualAnalysisFilesPresent:
							print 'Unable to find individual analysis files in: ' + individualMatFilesDir
							break
						# If the directory does not exist, we combine the calculations
						if not os.path.isdir(calculationsFullPath):
							functions.writeCombMatfileList(matFilesPath)						
							functions.CombineCalculationsinDirectory(tracker, matFilesPath, fullProjectDirPath)
						elif os.path.isdir(calculationsFullPath):
							# first we check if there's a matfile. If there's not, we re-run the combine analysis yo
							analysisFilePresent = False
							for (calcPath, calcDir, calcFnames) in os.walk(calculationsFullPath):
								for calcFname in calcFnames:
									if re.match('.*analysis\.mat',calcFname):
										analysisFilePresent = True
							mustReRun = functions.checkCombMatfileList(matFilesPath)
							if mustReRun or not analysisFilePresent:
								#delete figures directory
								functions.deleteFiguresPath(matFilesPath)
								functions.writeCombMatfileList(matFilesPath)	
								functions.CombineCalculationsinDirectory(tracker, matFilesPath, fullProjectDirPath)								
functions.runAllQsubsToCompletion()
						
		
		
