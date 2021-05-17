import numba
from numba.special import prange
import data_creation_v3
import datetime
import math
import pandas as pd
import numpy as np
import whois
from tqdm import tqdm
import os
print(os.getcwd())
os.chdir(os.getcwd()+'/FinalDataset/URL/')

@numba.jit(nopython=True, parallel=True)
def run():
    l = ['DefacementSitesURLFiltered.csv','phishing_dataset.csv','Malware_dataset.csv','spam_dataset.csv','Benign_list_big_final.csv']
    emp = data_creation_v3.UrlFeaturizer("").run().keys()
    A = pd.DataFrame(columns = emp)
    t=[]
    for r in prange(len(l)):
        j = l[r]
        print(j)
        d=pd.read_csv(j,header=None).to_numpy().flatten()
        for x in tqdm(prange(len(d))):
            i = d[x]
            temp=data_creation_v3.UrlFeaturizer(i).run()
            temp["File"]=j.split(".")[0]
            t.append(temp)
    A=A.append(t)
    os.chdir('../')
    A.to_csv("URL_features_v3.1.csv")

run()
