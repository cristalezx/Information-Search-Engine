
# coding: utf-8

# In[98]:

from index import *
from weighter import *
from irmodel import *


# In[90]:

from sklearn.metrics import mean_squared_error as mse
import copy
from numpy.random import sample
class RandomWalk:
    def __init__(self):
        return self
    def randomwalk(self):
        raise NotImplementedError('Always abstract class')       
class PageRank(RandomWalk):
    def __init__(self,max_iter,d):
        self.max_iter=max_iter
        self.d=d
    def randomwalk(self,linkout,linkin):
        self.mu={}
#         inital value
# linkout sortit de point i
# linkin enter in point i
# (V,E)=(all the document, link enter in this page =link in)

        N=len(linkout)*1.
        for page in linkout:
            self.mu[page]=1./N
        for t in range(self.max_iter):   
            mu_last=copy.deepcopy(self.mu)
            for i in linkout:
                Amu_i=0
                if linkin.has_key(i):
                    for j in linkin[i]:
                        Amu_i+=1.*self.mu[j]/len(linkout[j])# matrix compute
                self.mu[i]=1.*(1.-self.d)/N+self.d*Amu_i  
             
#            print mse(self.mu.values(),mu_last.values())*len(mu_last.values())
        return self.mu
    
class HITS(RandomWalk):
    def __init__(self,max_iter):
        self.max_iter=max_iter
    def randomwalk(self,linkout,linkin):
        self.a={}
        self.h={}
#         initial values
        for node in linkout:
            self.a[node]=1.
            self.h[node]=1.
        for t in range(self.max_iter):
            a_last=copy.deepcopy(self.a)
#             print a_last['1']
            h_last=copy.deepcopy(self.h)
            for i in linkout:         
                if linkin.has_key(i):
                    self.a[i]=np.sum(self.h[j] for j in list(linkin[i]))*1.
                    self.h[i]=np.sum(self.a[j] for j in list(linkout[i]))*1.   
                else:
                    self.a[i]=0.
                    self.h[i]=np.sum(self.a[j] for j in list(linkout[i])) *1.   
            a_norm=1.*np.linalg.norm(self.a.values(),ord=2)
            h_norm=1.*np.linalg.norm(self.h.values(),ord=2)
#             print self.a['593']
            for k in self.a:
                self.a[k]=1.*self.a[k]/a_norm
            for k in self.h:
                self.h[k]=1.*self.h[k]/h_norm
#             print float(self.a['593'])
#            print 4204*mse(self.a.values(),a_last.values())+4204*mse(self.h.values(),h_last.values())
        return self.a
from irmodel import *
class ModelRandomWork(IRmodel):
    def __init__(self,irmodel,index,weighter,randomwalk,nb_seeds,k):
        
#         random walk , model, index are instance
        self.weighter=weighter
        self.irmodel=irmodel
        self.nb_seeds=nb_seeds
        self.randomwalk=randomwalk
        self.k=k
        self.index=index   
        IRmodel.__init__(self,weighter)
    def getScores(self,query):
        print self.index
        docs=[]
#         three kinds of model: vector language okapi
        ranking=self.irmodel.getRanking(query)
    
        docs=[k for k,value in ranking]
#         inition VQ
        seeds=docs[:self.nb_seeds]
        V_Q=set() # unique value 
        V_Q=set(seeds)
        for i in range(self.nb_seeds):
            for j in self.weighter.index.linkout[seeds[i]]:
                V_Q.add(j)
            if self.weighter.index.linkin.has_key(seeds[i]) and (len(self.weighter.index.linkin[seeds[i]])>=k):
                V_Q |=set(random.sample(list(self.weighter.index.linkin[seeds[i]]),self.k if len(self.weighter.index.linkin[seeds[i]]) > self.k else len(self.weighter.index.linki[seeds[i]])))
        


        souslinkouts = {}
        souslinkins = {}
        for doc in V_Q:
            souslinkouts[doc] = set()
            if doc not in souslinkins:
                souslinkins[doc] = set()
            for s in self.weighter.index.linkout[doc]:
                if s in V_Q:
                    souslinkouts[doc].add(s)
                    if s not in souslinkins:
                        souslinkins[s] = set()
                    souslinkins[s].add(doc)
# random walk  is a instance already defined  
#         if self.randomWalk == 1:
#             rw = PageRank(0.85, 20)
#         else:
#             rw = HITS(20)
        self.scores = self.randomwalk.randomwalk(souslinkouts, souslinkins) 
        return self.scores
        
    
        


# In[99]:

# mrw=ModelRandomWork(irmodel=v,index=w.index,weighter=w,randomwalk=pr,nb_seeds=10,k=0)
# mrw.ModelGraphe("i love")


# In[76]:




# In[96]:

# pr=HITS(200)


# In[66]:

# from weighter import *
# from index import *
# w=WeighterTfTf()
# v=Vectoriel(weighter=w)
# v.construct()
# v.WeightsNormfordocs()


# In[67]:

# w.index.linkout


# In[ ]:




# In[ ]:



