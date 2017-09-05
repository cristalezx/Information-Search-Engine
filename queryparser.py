
# coding: utf-8

# In[1]:

get_ipython().magic(u'matplotlib inline')
import ParserCACM
from Parser import Parser
from porter import stem
from ParserCACM import ParserCACM


# In[3]:

import numpy as np
from irmodel import *
from weighter import *
from index import *


# In[4]:

from Parser import Parser
from Document import Document
#===============================================================================
# /**
#  * 
#  * Format of input files :
#  * .I <id>
#  * .A <Author>
#  * .W
#  * <Text>

#===============================================================================
class QueryParser(Parser):
    def __init__(self):
        '''
        Constructor
        '''
        Parser.__init__(self,".I")
    
    def getDocument(self,text):
        other={};
        modeA=False;
        modeW=False;
        info=""
        identifier=""
        author=""
        texte=""
        
        st=text.split("\n");
        s=""
        for s in st:
            if(s.startswith(".I")):
                identifier=s[3:]
                continue
            
            if(s.startswith(".")):
                if(modeW):
                    texte=info
                    info=""
                    modeW=False
                
                if(modeA):
                    author=info
                    info=""
                    modeA=False;         
            
            if(s.startswith(".W")):
                modeW=True;
                info=s[2:];
                continue;
            
            if(s.startswith(".A")):
                modeA=True;
                info=s[2:];
                continue;
            
            if((modeW) or (modeA)):
                #print "add "+s
                info+=" "+s
               
    
        if(modeW):
            texte=info;
            info="";
            modeW=False;
        
        if(modeA):
            author=info;
            info="";
            modeA=False;

        other["text"]=texte[4:]
        doc=Document(identifier,texte[2:],other);
        return doc      


# In[13]:

class Query():
    def __init__(self,id,text,relevants):
        self.id=id
        self.text=text
        self.relevants=relevants  
class QueryCACM(QueryParser):
    def __init__(self):
        QueryParser.__init__(self)
    def relevants(self):        
#       creat relevants
        f=open("cacm/cacm.rel")
        a={}
        for i in f:
            if i[0]=="0":
                key=i[1]
            else:
                key=i[:2]
            if a.has_key(key):
                a[key].append([i[j:7] for j in [3,4,5,6] if i[j]!="0"][0]) 
            else:
                a[key]=[[i[j:7] for j in [3,4,5,6] if i[j]!="0"][0]]
        self.relevants=a
        return self
    def nextQuery(self):
        doc=self.Q.nextDocument()       
        return Query(doc.getId(),doc.getText(),self.relevants[doc.getId()])
    def Querycacm(self):
        qp=QueryParser()
        qp.initFile("cacm/cacm.qry")
        query=qp.nextDocument()
        
        self.queries={}
        while query is not None:
            if query.getId() in self.relevants.keys():
                self.queries[query.getId()]=Query(query.getId(),query.getText(),self.relevants[query.getId()])
            else:
                self.queries[query.getId()]=Query(query.getId(),query.getText(),None)                
            query=qp.nextDocument()
        return self.queries              



# In[6]:

###  querty 里保存了所有query 包括有或者正确relevents的query  如果没有 relevents 就是None



# In[7]:

# query is an objet
class IRList:
    def __init__(self,query,doc_score):
        self.query=query
        self.doc_score=doc_score
    


# In[8]:

class EvalMeasure:
    def __init__(self):
        return
    def eval(self,irlist):
        raise NotImplementedError('always abstract class')
class PrecisionRecall(EvalMeasure):
#     nbLevels is a number not a rate
    def __init__(self,nbLevels=10):
        self.nbLevels=nbLevels
    def eval(self,irlist,nblevels=10):
        self.nbLevels=nblevels
        p=irlist.doc_score # all ranked docs        
        niveau=1./self.nbLevels
        nb_pertinent=0
        self.precision=[]
        self.recall=[]
        self.precision_recall=[]
        for i in range(len(p)):
            if irlist.doc_score[i][0] in irlist.query.relevants:
                nb_pertinent+=1.    
            self.precision.append(1.0*nb_pertinent/(i+1))
            self.recall.append(1.0*nb_pertinent/len(irlist.query.relevants))               
        j=0
        recalls=[]
        while niveau<1.and j<len(self.recall):
            if(self.recall[j]>=niveau):
                recalls.append(self.recall[j])
                self.precision_recall.append(np.max(self.precision[j:]))
                niveau += 1./self.nbLevels                                          
            else :
                j+=1
#         plt.scatter(self.recall,self.precision)    
        plt.plot(recalls,self.precision_recall,'-o')
        return self.precision_recall
    
class PrecisionMean(EvalMeasure):
    def eval(self,irlist):    
        nb_pertinent = 0
        precision_mean=[]
        self.precision=0
        self.recall=[]
        if irlist.query.relevants is  None:
            raise ValueError("We don't know the relevents of this query")
        else:
            for i in range(len(irlist.doc_score)) :

                    if irlist.doc_score[i][0] in irlist.query.relevants:
                        nb_pertinent += 1.             
                        self.precision += 1.*nb_pertinent/(i+1)
                        self.recall.append(1.0*nb_pertinent/len(irlist.query.relevants)) 
                        precision_mean.append(1.*self.precision/len(irlist.query.relevants))
            plt.plot(np.arange(len(precision_mean)),precision_mean) 
            self.precision_mean=precision_mean[-1]
        return self.precision_mean



# In[25]:

class EvalIRModel:
#     model: deifferent model of research on all the queries
#     evelu: different evaluation mesure "pr"=precision-recall or "pm"=precision moyenne
    def __init__(self,model,evalu="pr"):
        self.model=model
        self.evalu=evalu
    def eveluation (self,queries):
#         queries in created by querycacm
        results=[]

        for id_query in queries.keys():
            query=queries[id_query]
            if query.relevants !=None:
                print "jjjjj"
#                self.model.getRanking(query.text)
                irlist=IRList(query,self.model.getRanking(query.text))
                nblevels=1
                if self.evalu=='pr':    
                    mesure = PrecisionRecall(12)
                    nblevels=mesure.nbLevels
                elif self.evalu=='pm':
                    mesure = PrecisionMean()   
                results.append(mesure.eval(irlist))

        if self.evalu=='pr':
            self.mean=np.mean(results,axis=0)
            self.std=np.std(results,axis=0)                                       
            
        else:
            self.mean=np.mean(results)
            self.std=np.std(results)
        return self.mean,self.std
            
            
                
#         mean and variance       









