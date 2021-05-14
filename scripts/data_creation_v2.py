# -*- coding: utf-8 -*-

import datetime
import math
import pandas as pd
import numpy as np
import whois
from tqdm import tqdm
import os
os.chdir('../FinalDataset/URL/')
print(os.getcwd())
#os.chdir('/FinalDataset/URL/')

class UrlFeaturizer(object):
    
    def __init__(self, url):
        self.url = url
        self.domain = url.split('//')[-1].split('/')[0]
        self.today = datetime.datetime.now()

        try:
            self.whois = whois.whois(self.url)
        except:
            self.whois = None

    
    ## URL string Features
    def entropy(self):
        string = self.url.strip()
        prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
        entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])
        return entropy

    def numDigits(self):
        digits = [i for i in self.url if i.isdigit()]
        return len(digits)

    def urlLength(self):
        return len(self.url)

    def numParameters(self):
        params = self.url.split('&')
        return len(params) - 1

    def numFragments(self):
        fragments = self.url.split('#')
        return len(fragments) - 1

    def numSubDomains(self):
        subdomains = self.url.split('http')[-1].split('//')[-1].split('/')
        return len(subdomains)-1

    def domainExtension(self):
        ext = self.url.split('.')[-1].split('/')[0]
        return ext

    ## URL domain features
    def hasHttp(self):
        return 'http:' in self.url

    def hasHttps(self):
        return 'https:' in self.url
    
    #def urlIsLive(self):
     #   return self.response == 200

    def daysSinceRegistration(self):
        if self.whois!=None and "creation_date" in self.whois.keys() and self.whois['creation_date']!=None and type(self.whois['creation_date'])==str:
            d = self.whois['creation_date']
            #print(self.today - d)
            try:
                diff = self.today - d
            except:
                diff = self.today - d[0]
            diff = str(diff).split(' days')[0]
            #print(diff)
            return diff
        
        else:
            return -1

    def daysSinceExpiration(self):
        if self.whois!=None and "expiration_date" in self.whois.keys() and self.whois['expiration_date']!=None and type(self.whois['expiration_date'])==str:
            d = self.whois['expiration_date']
            try:
                diff =  d - self.today 
            except:
                diff = d[0] - self.today 
            diff = str(diff).split(' days')[0]
            return diff
        else:
            return -1

    ## URL Page Features
  
    def ip(self):
        string = self.url
        flag = False
        if ("." in string):
            elements_array = string.strip().split(".")
            if(len(elements_array) == 4):
                for i in elements_array:
                    if (i.isnumeric() and int(i)>=0 and int(i)<=255):
                        flag=True
                    else:
                        flag=False
                        break
        if flag:
            return 1 
        else:
            return 0

    def run(self):
        data = {}
        data['entropy'] = self.entropy()
        data['numDigits'] = self.numDigits()
        data['urlLength'] = self.urlLength()
        data['numParams'] = self.numParameters()
        data['hasHttp'] = self.hasHttp()
        data['hasHttps'] = self.hasHttps()
  
        data['ext'] = self.domainExtension()
        data['dsr'] = self.daysSinceRegistration()
        data['dse'] = self.daysSinceExpiration()
   
        data['num_%20'] = self.url.count("%20")
        data['num_@'] = self.url.count("@")
        data['has_ip'] = self.ip()
    
        return data
 
if __name__ == "__main__":
    
    l = ['DefacementSitesURLFiltered.csv','phishing_dataset.csv','Malware_dataset.csv','spam_dataset.csv','Benign_list_big_final.csv']

    emp =UrlFeaturizer("").run().keys()
    A = pd.DataFrame(columns = emp)
    t=[]
    for j in l:
        print(j)
        d=pd.read_csv(j,header=None)
        dd=d.to_numpy().flatten()
        for i in dd:
            temp=UrlFeaturizer(i).run()
            temp["File"]=j.split(".")[0]
            t.append(temp)
    A=A.append(t)
        #name = j.split("_")[0]
    os.chdir('../')
    A.to_csv("URL_features.csv")
