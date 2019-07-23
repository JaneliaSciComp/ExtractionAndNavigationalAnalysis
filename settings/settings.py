import re
import os
import pwd
import json

def get_username():
    return pwd.getpwuid( os.getuid() )[ 0 ]

config_dir = os.path.dirname(os.path.realpath(__file__))

cfg_file = open(config_dir + '/settings.cfg', 'r')
s = json.load(cfg_file)

settingsDir = s['Directory']['settingsDir']
mainProjectsPath = s['Directory']['pipelineDir']
zlaticProjectsPathString = s['Directory']['zlaticDirs']
zlaticProjectsPath = eval(zlaticProjectsPathString)
mmfTrackers = s['Trackers']['EXTRACT_MMF']
rubenTrackers = s['Trackers']['RUBEN_EXTRACT_MMF']
SPATIAL_TRACKERS = s['Trackers']['SPATIAL_TRACKERS']
projectsPath = [ mainProjectsPath ]
batchScriptDirProjectsSuffix = "/jobs.ignore/matlab/"
batchScriptDirZlatic = s['Directory']['zlaticClusterDir']


ignoreDirPat = re.compile('.*ignore.*')

# checkerboards to use
checkerboardsFileNames = {} 
camcalinfo = {}
matlabScriptFileName = {} 
matlabScriptComplete = {}
matlabScriptAnalysis = {} 
combineCalcs = {} 
supplementaryQsubParams = {}
extractionOptions = {}

rowNum = 0

for tracker in s['Files']:
    matlabScriptFileName[tracker] = settingsDir + '/' + s['Files'][tracker]['Process']
    matlabScriptComplete[tracker] = settingsDir + '/matlabBinaryLocation/' + s['Files'][tracker]['Complete']
    matlabScriptAnalysis[tracker] = settingsDir + '/' + s['Files'][tracker]['Analysis']
    combineCalcs[tracker] = settingsDir + '/' + s['Files'][tracker]['Combine']
    checkerboardsFileNames[tracker] = settingsDir + '/checkerboards/' + s['Files'][tracker]['Checkerboard']
    camcalinfo[tracker] = settingsDir + '/camcalinfos/' + s['Files'][tracker]['Camcalinfo']
    supplementaryQsubParams[tracker] = ''
    extractionOptions[tracker] = s['Files'][tracker]['ExtractionOptions']

mcrCacheRootBase = '/scratch/' + get_username() + '/'
mcrLocation = '/misc/local/matlab-2012b/'
sgeSyncPath = "/groups/zlatic/zlaticlab/code/choreography_plots/sge_sync.py"
