
# coding: utf-8


# In[6]:

from index import *
from irmodel import *
from weighter import *


# In[12]:

class Featurer :
    def __init__(self,):
        'constructor'
    def getFeatures(self,idDoc,query):
        raise NotImplementedError('Abstract class')


# In[13]:

class FeaturerDoc(Featurer):    
#     weighter is Weightertfidf instance   
    def __init__(self, weighter):
        self.featuredoc = {} #  key: idDoc  value: double list 
        self.weighter = weighter     
    def getFeatures(self, idDoc, query): 
        if idDoc not in self.docLengthFeature:
            features = []
            countWord = 0
            tf_doc = self.weighter.getDocWeightsForDoc(idDoc)
            len_doc=np.sum(tf_doc.values())
            nb_terms=len(tf_doc.keys())
            self.featuredoc[idDoc]=(len_doc,nb_terms)           
        return self.featuredoc[idDoc]
      


# In[14]:

class FeaturerQuery(Featurer):
#     weighter is Weightertfidf instance
    def __init__(self,weighter):
        self.weighter=weighter
        self.featuresqueryidflen={} #key: query dic value:(idf,len)
    def getFeatures(self,idDoc,query):
        ps=PorterStemmer()
        tf_query=ps.getTextRepresentation(query).values()
        querykey=tuple(tf_query.items())
        if querykey not in self.featuresqueryidflen.keys():
            idf_query=weighter.WeigtsForQuery(query)
            idf_sum=np.sum(idf_query.values())
            len_query=np.sum(querykey)
            self.featuresqueryidflen[querykey]=(idf_sum,len_query)
        return self.featuresqueryidflen[querykey]
        
        


# In[15]:

from TextRepresenter import TextRepresenter,PorterStemmer
class FeaturerModel(Featurer):
    def __init__(self,model,index,weighter):
        self.model=model
        self.index=index
        self.weighter=weighter
#         dic table features conserver les valeur calculer query as key
        self.featuredocquery={}  # key: query to key   {doc_id:score}
    def getFeatures(self,idDoc,query):
        ps=PorterStemmer()
        tf_query=ps.getTextRepresentation(query)
        querykey=tuple(tf_query.items())
#         ranking is a list dictionary  query is just text
        if querykey not in self.featuredocquery.keys() or (idDoc not in [f[0] for f in self.featuredocquery[querykey]]): 
            ranking=self.model.getRanking(query)
            self.featuredocquery[querykey]=ranking 
        return [ f[1] for  f in self.featuredocquery[querykey] if f[0]==idDoc][0]
       


# In[16]:

class FeaturerList(Featurer):
    def __init__(self, featurers):
        self.featurers = featurers      
    def getFeatures(self, idDoc, query):
        featuresList = []
        for featurer in self.featurers:
            featuresList.append(featurer.getFeatures(idDoc, query))          
        return featuresList
  


# In[17]:

# w=WeighterTfIdf()
# w.construct()
# w.getWeigtsForQuery('love love love weight id ')


# In[8]:

import numpy as np


# In[ ]:

from irmodel import *
from weighter import *
from index import *
from numpy.random import sample
import numpy as np


# In[18]:

from irmodel import *
class MetaModel(IRmodel):
    def __init__(self, featurerslist):
        self.FeaturersList = featurerslist       


# In[19]:

class LinearMetaModel(MetaModel):
    def __init__(self,index,featurerlist):
#         fetaurerlist can return  list of features
#         queries are objet of query 
        self.index=index
        self.max_iter=50
        self.alpha=1e-7
        self.lamda_l2=10-3
        self.featurerlist=featurerlist
        self.nb_feature=len(self.featurerlist.featurers)
        self.theta=np.zeros(self.nb_feature)*1.
    
    def sgd(self,queries):
        loss=0.0
        for t in range(self.max_iter):
            print t
            query=queries[np.random.choice(queries.keys())]
            if query.relevants!=None:          
                docpert=np.random.choice(query.relevants)
                docnonpert=np.random.choice(list(set(self.index.docs.keys())-set(query.relevants)))

                featurespert = self.featurerlist.getFeatures(docpert, query.text)
                featuresnonpert = self.featurerlist.getFeatures(docnonpert, query.text)
                
                scorepert=np.dot(self.theta,featurespert)
                scorenonpert=np.dot(self.theta,featuresnonpert)

               
                if (1 - scorepert + scorenonpert > 0):
                    self.theta+=list(self.alpha*np.asanyarray(([featurespert[i]-featuresnonpert[i] for i in range(self.nb_feature)])))   
                    
                  
                self.theta *= (1- 2 * self.alpha * self.lamda_l2)
                normtheta= np.linalg.norm(self.theta,ord=2)**2
                
                loss = max(0, 1 - scorepert + scorenonpert) + self.alpha * normtheta
        return self.theta,loss
            
    def getScores(self,query):
        scores={}
        for idDoc in self.index.docs:
            features = self.featurerlist.getFeatures(idDoc, query)
            scores[idDoc] = np.dot(self.theta,features)
        return scores
           




# In[ ]:

from queryparser import *


# In[10]:

from queryparser import *




