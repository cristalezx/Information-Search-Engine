
# coding: utf-8

# In[15]:

from irmodel import *
from index import *
from weighter import *
class LanguageModel(IRmodel):
    def __init__(self,lamda=0.5,weighter=Weighter()):
        self.lamda=lamda
        IRmodel.__init__(self,weighter)
    def prepare(self):
        self.l_corpus=0
        self.tf_docs={}
        self.tf_terminc={}
        for doc in self.weighter.index.docs.keys():
            tf_doc=self.weighter.index.getTfsForDoc(doc)
            self.tf_docs[doc]=tf_doc
            self.l_corpus+=np.sum(tf_doc.values())
        for term in self.weighter.index.stems.keys():
            self.tf_terminc[term]=np.sum([ j for (k,j) in self.weighter.getDocWeightsForStem(term).values()[0]])
            
        return self
        
        
    def getScores(self,query):
        scores={}
#         pmc pmd
        weights_query=self.weighter.getWeigtsForQuery(query)
        
        for doc_id in self.weighter.index.docs.keys():
            tf_d = self.tf_docs[doc_id]
            l_d=np.sum(tf_d.values())
            f_dq=0
            for term in weights_query:
                if term in self.weighter.index.stems.keys():
#                     tf_terminc   tf of term in all corpus
#                     if self.tf_terminc.has_key(term):
                    tf_terminc=self.tf_terminc[term]
#                     else:
#                         tf_terminc=np.sum([ j for (k,j) in self.weighter.getDocWeightsForStem(term).values()[0]])
#                         self.tf_terminc[term]=tf_terminc
                    pmc=1.*tf_terminc/self.l_corpus
                    if term in tf_d:
                        f_dq+=weights_query[term]+np.log(self.lamda*tf_d[term]/l_d+(1.-self.lamda)*pmc)
                    else:
                        f_dq+=weights_query[term]+np.log((1.-self.lamda)*pmc)
            scores[doc_id]=f_dq
        self.Scores=scores
        return self.Scores







