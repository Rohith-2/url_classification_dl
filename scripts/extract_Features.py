import data_creation_v3
import datetime
import math
import pandas as pd
import numpy as np
import whois
from tqdm import tqdm
from interruptingcow import timeout
import os
print(os.getcwd())
os.chdir('../FinalDataset/URL')

l = ['DefacementSitesURLFiltered.csv','phishing_dataset.csv','Malware_dataset.csv','spam_dataset.csv','Benign_list_big_final.csv']
#l = ['phishing_dataset.csv']


emp = data_creation_v3.UrlFeaturizer("").run().keys()
A = pd.DataFrame(columns = emp)
t=[]
for j in l:
    print(j)
    d=pd.read_csv(j,header=None).to_numpy().flatten()
    for i in tqdm(d):
        try: 
            with timeout(30, exception = RuntimeError):  
                temp=data_creation_v3.UrlFeaturizer(i).run()
                temp["File"]=j.split(".")[0]
                t.append(temp)
        except RuntimeError: 
            pass 
A=A.append(t)
os.chdir('../')
A.to_csv("features.csv")
