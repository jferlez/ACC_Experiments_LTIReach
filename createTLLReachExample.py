import numpy as np
import cdd
import TLLnet
import volestipy
import pickle
import sys
import datetime
import os
import tensorflow as tf
import importlib


def addTLLAndPathToExisting(instances,baseName='TLLExperiment',basePath=None):
    date_time = datetime.datetime.now().strftime('_%Y%m%d-%H%M%S')
    if basePath == None:
        basePath = './' + baseName + date_time
    basePath = basePath.rstrip('/')
    os.mkdir(basePath)
    os.mkdir(os.path.join(basePath,baseName))
    for k in range(len(instances)):
        instances[k]['basePath'] = basePath
        instances[k]['baseName'] = baseName + '_instance_' + str(k).zfill(int(np.log10(len(instances))+1)) + date_time
        instances[k]['TLLnetwork'] = instances[k]['baseName'] + '.tll'
        temp = {}
        temp['localLinearFns'] = instances[k]['TLLparameters']['localLinearFunctions']
        for out in range(len(temp['localLinearFns'])):
            temp['localLinearFns'][out][0] = temp['localLinearFns'][out][0].T
        temp['selectorSets'] = [ [ TLLnet.selectorMatrixToSet(sMat) for sMat in sOutputs] for sOutputs in instances[k]['TLLparameters']['selectorMatrices'] ]
        instances[k].pop('TLLparameters')
        temp['TLLFormatVersion'] = 1
        instances[k] = instances[k] | temp
        importlib.reload(tf)
        importlib.reload(TLLnet)

def saveAndGenerateMATLABInterface(experimentGroup,moduleName='TLLExperimentGroup'):
    if type(experimentGroup) != list or len(experimentGroup) == 0:
        print('Invalid experiment group')
        return
    for idx in range(len(experimentGroup)):
        if len(experimentGroup[idx]) > 0 and 'basePath' in experimentGroup[idx][0]:
            basePath = experimentGroup[idx][0]['basePath']
        else:
            print('Invalid problem group...')
            return
        date_time = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        moduleName = moduleName + date_time
        with open( os.path.join(  basePath ,  moduleName + '.p'),'wb') as fp:
            pickle.dump(experimentGroup,fp,protocol=pickle.HIGHEST_PROTOCOL)
        os.popen('cp run_experiment.py ' + basePath)
        with open(os.path.join(basePath, 'run_experiment.sh'), 'w') as fp:
            print('#!/bin/bash\n\
SCRIPT_DIR=$( cd -- \"$( dirname -- \"${BASH_SOURCE[0]}\" )\" &> /dev/null && pwd )\n\
cd ..\n\
git pull\n\
cd \"$SCRIPT_DIR\"\n\
charmrun +p1 run_experiment.py ' + moduleName + '.p' + '\n\
ssh 10.0.0.10 \"mkdir -p /media/azuredata/' + basePath + '\"\n\
scp -r ~/acc23ltireach/' + basePath + ' 10.0.0.10:/media/azuredata/' + basePath + '\n\
pwsh ~/shutdown_self.ps1', file=fp)
        os.popen('chmod 755 ' + os.path.join(basePath, 'run_experiment.sh'))


if __name__=='__main__':

    # mytll = TLLnet(input_dim=2,linear_fns=7,uo_regions=20)

    # mat = mytll.selectorMatFromSet(frozenset([1,5,6]))

    # print(mat)

    # mytll.generateRandomCPWA()

    # print(mytll.getLocalLinFns())

#     poly = generatePolytope(2,20)

#     # print(poly)

#     with open('testFile' + str(1).zfill(5) + '.p','wb') as fp:
#         pickle.dump([poly,2],fp,protocol=pickle.HIGHEST_PROTOCOL)
    
#     with open('testFileModule' + str(1).zfill(5) + '.py','wb') as fp:
#         fp.write(b'\n\
# import pickle\n\
# def f(path):\n\
#     with open(path+\'/testFile00001.p\', \'rb\') as fp:\n\
#         retVal = pickle.load(fp)\n\
#     return retVal\n\
#         \n')


    # # PROBLEM LIST 0
    # idx = 0
    # for k in range(len(problemList[idx])):
    #     problemList[idx][k] = generateTLLProblem(n=1,m=1,N=100,M=60)
    # generateTLLExperiment(problemList[idx],baseName='TLLexper_n1m1N100M60_')
    # print('Done with PROBLEM LIST 0')

    with open('sizeVsTime_n2_input.p','rb') as fp:
        originalExperiment = pickle.load(fp)

    problemList = []
    for jj in range(4):
        for ii in range(10):
            problemList.append([originalExperiment[jj][ii]])
    
    for idx in range(len(problemList)):
        addTLLAndPathToExisting(problemList[idx],basePath='minion' + str(idx))


    # Generate a list for this problem group:
    # problemList = [[{} for k in range(50)] for i in range(4)]

    # # PROBLEM LIST 0
    # idx = 0
    # generateTLLExperimentFlat(problemList[idx],baseName='TLLexper_n1m1N32M32_',n=1,m=1,N=32,M=32)
    # print('Done with PROBLEM LIST 0')

    # # PROBLEM LIST 0
    # idx = 1
    # generateTLLExperimentFlat(problemList[idx],baseName='TLLexper_n1m1N64M48_',n=1,m=1,N=64,M=48)
    # print('Done with PROBLEM LIST 0')

    # # PROBLEM LIST 0
    # idx = 2
    # generateTLLExperimentFlat(problemList[idx],baseName='TLLexper_n2m1N32M32_',n=2,m=1,N=32,M=32)
    # print('Done with PROBLEM LIST 0')

    # # PROBLEM LIST 0
    # idx = 3
    # generateTLLExperimentFlat(problemList[idx],baseName='TLLexper_n2m1N64M48_',n=2,m=1,N=64,M=48)
    # print('Done with PROBLEM LIST 0')

    # # PROBLEM LIST 1
    # idx = 1
    # for k in range(len(problemList[idx])):
    #     problemList[idx][k] = generateTLLProblem(n=2,m=1,N=15,M=40)
    # generateTLLExperiment(problemList[idx],baseName='TLLexper_n2m1N15M40_')
    # print('Done with PROBLEM LIST 1')

    # # PROBLEM LIST 2
    # idx = 2
    # for k in range(len(problemList[idx])):
    #     problemList[idx][k] = generateTLLProblem(n=2,m=1,N=128,M=100)
    # generateTLLExperiment(problemList[idx],baseName='TLLexper_n2m1N128M100_')
    # print('Done with PROBLEM LIST 2')

    # Create a MATLAB interface for this problem group:
    for idx in range(len(problemList)):
        saveAndGenerateMATLABInterface([problemList[idx]])

    pass