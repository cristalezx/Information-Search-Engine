
# coding: utf-8

# In[1]:

import numpy as np
import matplotlib.pyplot as plt
from Parser import Parser
from Document import Document
from porter import stem
from ParserCACM import ParserCACM
from TextRepresenter import TextRepresenter,PorterStemmer


# In[9]:

from weighter import *
from index import Index


# In[13]:

class IRmodel:
    def __init__(self,weighter=Weighter(),index=Index()):
        self.weighter=weighter
        self.index=Index()
    def construct(self):
        self.weighter.construct()
    def getScores(self,query):
        raise NotImplementedError("This is a abstract class!")
    def getRanking(self,query):
        self.Scores=self.getScores(query)
        self.Rank=sorted(self.Scores.iteritems(),key= lambda d:d[1],reverse=True)   
        return self.Rank


# In[56]:

import time
class Vectoriel(IRmodel):
# normalised: bool
# Weighter: class objet
    def __init__(self,normalised=False,weighter=Weighter()):
        self.normalised=normalised
        self.weighter=weighter
        IRmodel.__init__(self,weighter)
    def WeightsNormfordocs(self):
        self.weightsdocs={}
        self.normsdocs={}
        for doc_id in self.weighter.index.docs.keys():  
            D_Weights=self.weighter.getDocWeightsForDoc(doc_id)
            self.weightsdocs[doc_id]=D_Weights 
            D_norm=np.linalg.norm(D_Weights.values(),ord=1)*1.
            self.normsdocs[doc_id]=D_norm
        return self
            
    def getScores(self,query):
        Q_Weights=self.weighter.getWeigtsForQuery(query)      
        scores={}
        if (self.normalised==False):
            t0=time.time()
            for doc_id in self.weighter.index.docs.keys():
                D_Weights=self.weightsdocs[doc_id]     
                score=sum(Q_Weights[k]*D_Weights[k] for k in Q_Weights if k in D_Weights)            
                scores[doc_id]=score
            print  "Calculate time is:",time.time()-t0
            self.Scores=scores      
            return self.Scores
        else:
            Q_norm=np.linalg.norm(Q_Weights.values(),ord=1)*1.
            for doc_id in self.weighter.index.docs.keys():
                D_Weights=self.weightsdocs[doc_id]   
                D_norm=self.normsdocs[doc_id]
                score=sum(Q_Weights[k]*D_Weights[k] for k in Q_Weights if k in D_Weights) 
                scores[doc_id]=score/(D_norm*Q_norm)
            self.Scores=scores      
            return self.Scores


# In[66]:

# exemple
# v=Vectoriel(weighter=WeighterTf1(),normalised=True)
# v.construct()


# In[ ]:



