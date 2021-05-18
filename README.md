# Url Classification 
### 19AIE211-Introduction to Computer Networks End Project   
Authors:  
> [Aaditya Jain](https://github.com/aadityajain1)    
> [Anirudh Bhaskar](https://github.com/AnirudhBhaskar21)    
> [Srikanth]( https://github.com/Srikanth-AIE)    
> [Rohith Ramakrishnan](https://github.com/Rohith-2)
<hr style=\"border:0.5px solid gray\"> </hr>

## Set-Up:
Pre-requisites : conda and git  
Please Note : All System Paths in the scripts, are coded in UNIX OS format, please convert '/' to "\\" for Windows OS.
```
git clone https://github.com/Rohith-2/url_classification_dl.git
cd url_classification_dl
conda create -n pyenv python=3.8
conda activate pyenv
pip install -r requirements.txt
```
Training :    
```
cd scripts/
python extract_Features.py
```

<hr style=\"border:0.5px solid gray\"> </hr>    

## References:  
https://towardsdatascience.com/predicting-the-maliciousness-of-urls-24e12067be5  

> We would like to thank our professor [Premjith B](https://github.com/premjithb) for the assistance and guidance.    


