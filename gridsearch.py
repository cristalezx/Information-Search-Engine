
# coding: utf-8

# In[2]:

from irmodel import  *
from weighter import *
from index import *
import numpy as np
from queryparser import *


# In[3]:

class GridSearch:
    def __init__(self,irmodel,evalmeasure,queries,weighter):
#         irmodel is just langue or okapi
        self.irmodel=irmodel
        self.evalmeasure=evalmeasure
        self.queries=queries
        self.weighter=weighter
    def optimisation(self):# List of parameters
# parameters: lambda for kanguage model, k and b for Okapi
        bestparas=[]
        bestscore=0
        if self.irmodel=='langue':     
            lamdas=np.arange(0,1,0.1)
            for lamda in lamdas:
                lm=LanguageModel(lamda=lamda)
                em=EvalIRModel(model=lm,evalu=self.evalmeasure)
                mean,std=em.eveluation (self.queries)
                if np.sum(mean)>bestscore:
                    bestscore=np.sum(mean)
                    bestparas=lamda

        if self.irmodel=='okapi': 
            ks=np.arange(1.0, 2.0, 0.2)
            bs=np.arange(0.7, 0.8, 0.01)
            for k in ks :
                for b in bs:
                    lm=OkapiModel(k1=k,b=b)
                    em=EvalIRModel(model=lm,evalu=self.evalmeasure)
                    mean,std=em.eveluation (self.queries)
                    if np.sum(mean)>bestscore:
                        bestscore=np.sum(mean)
                        bestparas=[k,b]
        print 'BestParameters for model:'+str(self.irmodel)+"are/is:"+bestparas

        return bestparas
    

