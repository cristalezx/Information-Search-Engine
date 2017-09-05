
# coding: utf-8


# In[2]:

from weighter import *
from index import *
from irmodel import *
class OkapiModel(IRmodel):
    def __init__(self,k1=1,b=0.75,weighter=Weighter()):
        self.k1=k1
        self.b=b
        IRmodel.__init__(self,weighter)
    def prepare(self):
        L=0
        self.N=len(self.weighter.index.docs) 
        self.tf_docs={}
        self.df_t={}
        for doc_id in self.weighter.index.docs.keys():
            tf_doc=self.weighter.getDocWeightsForDoc(doc_id)
            self.tf_docs[doc_id]=tf_doc
            L+=np.sum(tf_doc.values())
        self.L_mean=1.*L/self.N
        for term in self.weighter.index.stems.keys():
            self.df_t[term]=len(self.weighter.getDocWeightsForStem(term)) 
        return self
      
    def getScores(self,query):
        weights_query=self.weighter.getWeigtsForQuery(query)          
        self.scores={}
        for doc_id in self.weighter.index.docs.keys():
            tf_d=self.tf_docs[doc_id]
            L_d=np.sum(tf_d.values())
            f_dq=0.
            for t in weights_query.keys():
                 if t in self.weighter.index.stems.keys():
                        df_t=self.df_t[t]
                        idf=max(0,np.log(1.*(self.N-df_t+0.5)/(df_t+0.5)))  
                        if t in tf_d.keys():             
                            f_dq+=idf*((self.k1+1)*tf_d[t])/((1.-self.b+self.b*L_d/self.L_mean)*self.k1+tf_d[t])
                        else:
                            f_dq+=0
            self.scores[doc_id]=f_dq
        return self.scores













