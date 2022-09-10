
import charm4py
from charm4py import charm, Chare, Channel, coro, Group, Future
import numpy as np
import pickle
import time
import sys

import LTITLLReach
import TLLnet

charm.options.local_msg_buf_size = 10000


class Main(Chare):
    @coro
    def __init__(self,args):

        if len(sys.argv) != 2:
            print('ERROR: incorrect number of arguments!')
            return

        
        with open(sys.argv[1], 'rb') as fp:
            expers = pickle.load(fp)


        pes = {'poset':[(0,1,1)],'hash':[(0,1,1)]}
        reach = Chare(LTITLLReach.LTITLLReach,args=[pes],onPE=0)
        charm.awaitCreation(reach)

        

        for sizeIdx in range(len(expers)):
            for experIdx in range(len(expers[sizeIdx])): #range(len(expers[sizeIdx])):

                myExperiment = expers[sizeIdx][experIdx]

                tllController = TLLnet.TLLnet.fromTLLFormat(myExperiment)

                print('Working on sizeIdx ' + str(sizeIdx) + ', instanceIdx ' + str(experIdx))
                t = time.time()
                optsDict = { \
                        'method':'fastLP', \
                        'solver':'glpk', \
                        'useQuery':False, \
                        'hashStore':'bits', \
                        'useNumba':True, \
                        'minimalSimplexQtys':False, \
                        'prefilter':False, \
                        'tol':1e-9, \
                        'rTol':1e-9, \
                        'verbose':False \
                    }
                retVal = reach.initialize( \
                                tllController=tllController, \
                                A=myExperiment['system']['A'], \
                                B=myExperiment['system']['B'], \
                                polytope=myExperiment['inputPoly'] \
                            )

                T = 3
                myExperiment['reach'] = {}
                myExperiment['reach']['reach'] = reach.computeLTIReach( \
                                T=T, epsilon=0.2, \
                                opts=optsDict, \
                                ret = True \
                            ).get()

                reachSamples = reach.computeReachSamples(myExperiment['samples']['input'], T=T, reachBoxes=myExperiment['reach']['reach'], ret=True).get()
                myExperiment['reach']['reachSamples'] = reachSamples                

                

                print('Time to enumerate regions is: ' + str(time.time()-t))

                with open('results_' + sys.argv[1], 'wb') as fp:
                    pickle.dump(expers,fp)

        charm.exit()

charm.start(Main,modules=['posetFastCharm','DistributedHash','TLLHypercubeReach','LTITLLReach'])
