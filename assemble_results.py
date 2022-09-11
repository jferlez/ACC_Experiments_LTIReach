
import numpy as np
import pickle
import os
import sys
import re
import h5py

if __name__ == '__main__':

    resultsDir = os.path.abspath( \
            os.path.join( \
                os.path.dirname( os.path.abspath(sys.argv[0]) ),
                '..', \
                'results/ltireach' \
            ) \
        )
    resultsOutputFile = os.path.join(resultsDir,'results_ltireach.p')

    baseName = 'minion'
    experGroupName = 'TLLExperimentGroup'

    dirList = [ \
            'eps=0.1' \
        ]
    numExperimentsPerGroup = 10
    results = {}

    for d in dirList:
        r = os.path.join(resultsDir, d)
        if not os.path.isdir(r):
            print(f'ERROR: {d} is not a valid directory... skipping...')
            continue

        workerContents = os.listdir(r)

        for pname in workerContents:
            checkName = re.match(r'^' + baseName + r'([0-9]+)$', os.path.basename(pname))
            if not os.path.isdir(os.path.join(r,pname)) or not checkName or not os.path.isdir(os.path.join(r,pname,pname)):
                continue
            workerIdx = int(checkName.group(1))
            sizeIdx = workerIdx // numExperimentsPerGroup
            experIdx = workerIdx % numExperimentsPerGroup
            if not sizeIdx in results:
                results[sizeIdx] = {}
            if experIdx in results[sizeIdx]:
                print('ERROR: duplicate experiment in experiment group...')
                exit(1)
            results[sizeIdx][experIdx] = {}
            results[sizeIdx][experIdx]['reach'] = {}

            contents = os.listdir(os.path.join(r,pname,pname))
            resultsFile = None
            for fname in contents:
                if re.match(r'^results_' + experGroupName + r'.*\.p$',os.path.basename(os.path.join(r,pname,pname,fname))):
                    resultsFile = os.path.join(r,pname,pname,fname)
                    break

            if resultsFile is None:
                print(f'ERROR: no matching .p file in {os.path.join(r,pname)}')
                logFile = None
                numSteps = None
                for fname in contents:
                    if fname == 'log.out' and os.path.isfile(os.path.join(r,pname,pname,'log.out')):
                        logFile = os.path.join(r,pname,pname,'log.out')
                        with open(logFile) as fp:
                            log = fp.readlines()
                        numSteps = 0
                        for ln in log:
                            if re.search('T=',ln):
                                numSteps += 1
                        results[sizeIdx][experIdx]['reach']['numSteps'] = numSteps
                        results[sizeIdx][experIdx]['reach']['incomplete'] = True
                if logFile is None:
                    print(f'ERROR: No log file found in {os.path.join(r,pname)}')
                    continue
            else:
                temp = {}
                with open(resultsFile,'rb') as fp:
                    temp = pickle.load(fp)[0][0]
                if 'reach' in temp and type(temp['reach']) is dict and 'reach' in temp['reach'] and type(temp['reach']['reach']) is dict:
                    temp['reach']['timeElapsed'] = 0
                    for ky in temp['reach']['reach'].keys():
                        if 'time' in temp['reach']['reach'][ky]:
                            temp['reach']['timeElapsed'] += temp['reach']['reach'][ky]['time']
                        else:
                            print(f'Missing execution time for step {ky} of sizeIdx = {sizeIdx}, experIdx = {experIdx}')
                    temp['reach']['valid'] = True
                    temp['reach'] = temp['reach'] | results[sizeIdx][experIdx]['reach']

                    results[sizeIdx][experIdx] = temp
                else:
                    results[sizeIdx][experIdx] = temp | results[sizeIdx][experIdx]

            # print(results[sizeIdx][experIdx]['reachNNV'])
            # print(f'{baseName}{workerIdx} --> [{sizeIdx}][{experIdx}] --> {resultsFile}')
    with open(resultsOutputFile,'wb') as fp:
        pickle.dump(results, fp)

