
# coding: utf-8

# In[49]:

# import import_ipynb
import numpy as np
from Parser import Parser
from Document import Document
from porter import stem
from ParserCACM import ParserCACM
from TextRepresenter import TextRepresenter,PorterStemmer


# In[2]:

from index import Index


# In[17]:

class Weighter: 
    def __init__(self,index=Index()):
        self.index=index
    def construct(self):
        self.index.indexation()
        return self
    def getDocWeightsForDoc(self,doc_id):
        raise NotImplementedError("This is a abstract class!")
    def getDocWeightsForStem(self,stem):
        raise NotImplementedError("This is a abstract class!")      
    def getWeigtsForQuery(self,query):
        raise NotImplementedError("This is a abstract class!")


# In[19]:

class WeighterTf1(Weighter):
    def __init__(self):
        Weighter.__init__(self)
    def getDocWeightsForDoc(self,doc_id):
        return self.index.getTfsForDoc(doc_id)
    def getDocWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)           
    def getWeigtsForQuery(self,query):
        ps=PorterStemmer()
        self.Weights_Query={}.fromkeys(ps.getTextRepresentation(query).keys(),1) 
        return self.Weights_Query


# In[26]:

class WeighterTfTf(Weighter):
    def __init__(self):
        Weighter.__init__(self)
    def getDocWeightsForDoc(self,doc_id):
        return self.index.getTfsForDoc(doc_id)
    def getDocWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)           
    def getWeigtsForQuery(self,query):
        ps=PorterStemmer()
        return ps.getTextRepresentation(query)
    


# In[53]:

class WeighterTfIdf(Weighter):
    def __init__(self):
        Weighter.__init__(self)
    def getDocWeightsForDoc(self,doc_id):
        return self.index.getTfsForDoc(doc_id)
    def getDocWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)           
    def getWeigtsForQuery(self,query):
        ps=PorterStemmer()
        nb_doc=len(self.index.docs)   
        tf_q=ps.getTextRepresentation(query)      
        return {stem:np.log(nb_doc/(1+len(self.index.getTfsForStem(stem).values()[0]))) for stem in tf_q.keys()}


# In[72]:

class WeighterLogtfIdf(Weighter):
    def __init__(self):
        Weighter.__init__(self)
    def getDocWeightsForDoc(self,doc_id):
        tf_d=self.index.getTfsForDoc(doc_id)
        return {stem: 1+np.log(tf_d[stem]) for stem in tf_d.keys()}
    def getDocWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)           
    def getWeigtsForQuery(self,query):
        ps=PorterStemmer()
        nb_doc=len(self.index.docs)   
        tf_q=ps.getTextRepresentation(query)      
        return {stem:np.log(nb_doc/(1+len(self.index.getTfsForStem(stem).values()[0]))) for stem in tf_q.keys()}


# In[78]:

class WeighterLogtfidfLogtfidf(Weighter):
    def __init__(self):
        Weighter.__init__(self)
    def getDocWeightsForDoc(self,doc_id):
        nb_doc=len(self.index.docs)
        tf_d=self.index.getTfsForDoc(doc_id)
        idf_d={stem:np.log(nb_doc/(1+len(self.index.getTfsForStem(stem).values()[0]))) for stem in tf_d.keys()}
        return {stem: (1+np.log(tf_d[stem]))*idf_d[stem] for stem in tf_d.keys()}
    def getDocWeightsForStem(self,stem):
        return self.index.getTfsForStem(stem)           
    def getWeigtsForQuery(self,query):
        ps=PorterStemmer()
        nb_doc=len(self.index.docs)  
        tf_q=ps.getTextRepresentation(query)
        idf_q={stem:np.log(nb_doc/(1+len(self.index.getTfsForStem(stem).values()[0]))) for stem in tf_q.keys()}
        return {stem: (1+np.log(tf_q[stem]))*idf_q[stem] for stem in tf_q.keys()}
       

