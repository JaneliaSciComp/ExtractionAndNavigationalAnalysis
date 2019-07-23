import json
import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Load Larval Data")
    parser.add_argument('--zlatic_dirs', dest='zlatic_dirs', default='', type=str, help='name zlatic dirs')
    parser.add_argument('--zlatic_cluster_scripts', dest='zlatic_cluster_scripts', default='', type=str, help='name for cluster scripts for zlatic lab')
    parser.add_argument('--pipeline_dir', dest='pipeline_dir', default='', type=str, help='name pipeline dir')
    parser.add_argument('--settings_dir', dest='settings_dir', default='', type=str, help='name settings dir')
    args = parser.parse_args()

    ojson = {
        "Directory": {
            "settingsDir" : args.settings_dir,
            "pipelineDir" : args.pipeline_dir,
            "zlaticDirs" : args.zlatic_dirs,
            "zlaticClusterDir" : args.zlatic_cluster_scripts,
        },
        "Trackers": {
            "EXTRACT_MMF" : ['t7', 't8', 't9', 't10', 't14'],
            "RUBEN_EXTRACT_MMF" : ['t16'],
            "SPATIAL_TRACKERS" : ['t7', 't9', 't10', 't14'],
        },
        "Files": {
            't1': {
                'Process' : 'run_MWTtoMatFiles.sh',
                'Analysis' : 'run_Spatial_Tihana.sh',
                'Combine' : 'run_CombineSpatialCalcs.sh',
                'Complete' : '',
                'Project' : '',
                'Checkerboard' : '',
                'Camcalinfo' : '',
                'ExtractionOptions': {}
            },
            't7': {
                'Process' : 'run_processDirToMat.sh',
                'Analysis' : 'run_Spatial.sh',
                'Combine' : 'run_CombineSpatialCalcs.sh',
                'Complete' : '',
                'Project' : 'ThermotaxisScreen',
                'Checkerboard' : 't7_checkerboard_20120119.png',
                'Camcalinfo' : 'camcalinfo_t07_20120119.mat',
                'ExtractionOptions' : {
                    'padding': 0,
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 999999,
                    'minArea': 5,
                    'maxArea': 2000,
                    'overallThreshold': 25,
                    'winSize': 51,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2000,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, 2000, 2000 ]
                },
            },
            't8': {
                'Process' : 'run_processDirToMat.sh',
                'Analysis' : 'run_Temporal.sh',
                'Combine' : 'run_CombineTemporalCalcs.sh',
                'Complete' : '',
                'Project' : 'PhototaxisScreen',
                'Checkerboard' : 't8_checkerboard_20120119.png',
                'Camcalinfo' : 'camcalinfo_t08_20120119.mat',
                'ExtractionOptions' : {
                    'padding': 0,
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 999999,
                    'minArea': 5,
                    'maxArea': 2000,
                    'overallThreshold': 25,
                    'winSize': 51,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2000,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, 2000, 2000 ]
                },

            },
            't9': {
                'Process' : 'run_processDirToMat.sh',
                'Analysis' : 'run_Spatial.sh',
                'Combine' : 'run_CombineSpatialCalcs.sh',
                'Complete' : '',
                'Project' : '',
                'Checkerboard' : '',
                'Camcalinfo' : 'camcalinfo_t09_20111025_flipx_t_flipy_t.mat',
                'ExtractionOptions' : {
                    'padding': 0,
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 999999,
                    'minArea': 5,
                    'maxArea': 2000,
                    'overallThreshold': 25,
                    'winSize': 51,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2000,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, 2000, 2000 ]
                },
            },
            't10': {
                'Process' : 'run_processDirToMat.sh',
                'Analysis' : 'run_Spatial.sh',
                'Combine' : 'run_CombineSpatialCalcs.sh',
                'Complete' : '',
                'Project' : '',
                'Checkerboard' : '',
                'Camcalinfo' : 'camcalinfo_t10_20111025_flipx_t_flipy_t.mat',
                'ExtractionOptions' : {
                    'padding': 0,
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 999999,
                    'minArea': 5,
                    'maxArea': 2000,
                    'overallThreshold': 25,
                    'winSize': 51,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2000,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, 2000, 2000 ]
                },
            },
            't11': {
                'Process' : 'run_MWTtoMatFiles_Louis.sh',
                'Analysis' : 'run_processLouis.sh',
                'Combine' : 'run_combineSpatialCalcs_Louis.sh',
                'Complete' : '',
                'Project' : '',
                'Checkerboard' : '',
                'Camcalinfo' : '',
                'ExtractionOptions': {}
            },
            't14': {
                'Process' : 'run_processDirToMat.sh',
                'Analysis' : 'run_Spatial.sh',
                'Combine' : 'run_CombineSpatialCalcs.sh',
                'Complete' : '',
                'Project' : 'odor',
                'Checkerboard' : '',
                'Camcalinfo' : 'camcalinfo_from_marc_20130313.mat',
                'ExtractionOptions' : {
                    'padding': 0,
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 999999,
                    'minArea': 5,
                    'maxArea': 2000,
                    'overallThreshold': 25,
                    'winSize': 51,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2000,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, 2816, 2816 ]
                },
            },
            't16': {
                'Process' : '',
                'Analysis' : '',
                'Combine' : '',
                'Complete' : 'run_processDirToMatRuben.sh',
                'Project' : 'ruben',
                'Checkerboard' : '',
                'Camcalinfo' : 'camcalinfo_t16_20141115.mat',
                'ExtractionOptions' : {
                    'verbosityLevel': 2,
                    'startFrame': 0,
                    'endFrame': 20*60*30,
                    'maxFrames': 21600, #12*60*30/
                    'minArea': 20,
                    'maxArea': 1600,
                    'overallThreshold': 30,
                    'winSize': 50,
                    'nBackgroundFrames': 5,
                    'background_resampleInterval': 2800,
                    'maxExtractDist': 20,
                    'showExtraction': 'true',
                    'extension': 'mmf',
                    'padding': 0,
                    'background_blur_sigma': 0,
                    'thresholdScaleImage': '',
                    'blurThresholdIm_sigma': 10,
                    'frameNormalizationMethod': 0,
                    'imStackLength': 0,
                    'maxExtractDist': 15,
                    'showExtraction': 'false',
                    'maxMaggotContourAngle': 1.5708,
                    'analysisRectangle': [ 0, 0, -1, -1 ]
                },
            },
            't110': {
                'Process' : 'run_MWTtoMatFiles_Louis.sh',
                'Analysis' : 'run_processLouis.sh',
                'Combine' : 'run_combineSpatialCalcs_Louis.sh',
                'Complete' : '',
                'Project' : '',
                'Checkerboard' : '',
                'Camcalinfo' : '',
                'ExtractionOptions': {}
            },
        }
    }

    outfile = open('settings/settings.cfg', 'w')
    outfile.write(json.dumps(ojson))
    outfile.close()