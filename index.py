
# coding: utf-8

# In[ ]:

# TME1 class Index


# In[9]:

import numpy as np
from Parser import Parser
from Document import Document
from porter import stem
from ParserCACM import ParserCACM
from TextRepresenter import TextRepresenter,PorterStemmer


# In[68]:

class Index:
    def __init__(self,name=[],docs=[],stems=[],docFrom=[],parser=[],textRepresenter=[]):
        self.name=name
        self.docs=docs
        self.docFrom=docFrom
        self.stems=stems
        self.parser=parser
        self.textRepresenter=textRepresenter
    def indexation(self):
## Creat docs and stems docFrom
        self.docs=CreatDocs()
        self.stems=CreatTerms()
        self.docFrom=CreatdocFrom()
        self.parser=ParserCACM()
        self.texRepresenter=PorterStemmer() 
        self.linkin,self.linkout=createlink()
        return self
    def getTfsForDoc(self,doc_id):
        f=open("_index.txt",'r')
        f.seek(self.docs[doc_id][0])
        Tfs_dic=eval("{"+f.read(self.docs[doc_id][1])+"}")  
        
        return Tfs_dic[doc_id][0]
    def getTfsForStem(self,stem):
        f=open("_inversed.txt",'r')
        f.seek(self.stems[stem][0])
        return eval("{"+f.read(self.stems[stem][1])+"}")       
    def getStrDoc(self,doc_id): 
        f=open("cacm/cacm.txt",'r')
        f.seek(self.docFrom[doc_id][0])       
        return f.read(self.docFrom[doc_id][1]).split('\n')

def CreatDocs():
    h=open('_index.txt','r+')
    for i in h:
        i=i
    a=i[1:-2].split("], ")
    position=1
    length=0
    dic={}
    for i in range(0,len(a)):
        if i==0:
            key=a[i].split(":")
            length=len(a[i])+1
            dic[str(key[0])[1:-1]]=[1,length]
        
        else:
            key=a[i].split(":")
            length=len(a[i])+1
            position=position+len(a[i-1])+3            
            dic[key[0][1:-1]]=(position,length)   
    return dic

def CreatTerms():
    g=open('_inversed.txt','r')
    for i in g:
        i=i
    a=i[1:-1].split("], ")
    dic={}
    position=1
    length=0
    for i in range(0,len(a)):
        if i==0:
            key=a[i].split(":")
            length=len(a[i])+1
            dic[key[0][1:-1]]=[1,length]
        elif i==(len(a)-1):
            key=a[i].split(":")
            length=len(a[i])+1
            position=position+len(a[i-1])+3
            dic[key[0][1:-1]]=(position,length-1)
        else:
            key=a[i].split(":")
            length=len(a[i])+1
            position=position+len(a[i-1])+3            
            dic[key[0][1:-1]]=(position,length)           
    return dic

def CreatdocFrom():
    f=open("cacm/cacm.txt",'r+')
    docFrom={}
    length_all=[]
    keys=[]
    length=0
    position=0
    for i in f:
        if i[:2]==".I": 
            docFrom[i[3:-1]]=[position,]
            keys.append(i[3:-1])
            length_all.append(length)
            length=0
        position=position+ len(i) 
        length=length+len(i)
    length_all.append(length)   
    for i in range(len(keys)):
        docFrom[keys[i]].append(length_all[i+1])
    return docFrom

def createlink():
    linkout={}
    linkin={}
    ps=ParserCACM()
    ps.initFile("cacm/cacm.txt")
    doc=ps.nextDocument()
    while doc:
        linkout[doc.getId()]=set()
        links=doc.get('links').split(';')
        for link in links:
            if link!='':
                linkout[doc.getId()].add(link)
                if link not in linkin:
                    linkin[link]=set()    # value unique            
                linkin[link].add(doc.getId())                             
        doc=ps.nextDocument() 
    return linkin,linkout




