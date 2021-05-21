# Url Feature Extraction & Classification 
### 19AIE211-Introduction to Computer Networks End Project   
Using Neural Networks to classify various URLs  
  
Authors:  
> [Aaditya Jain](https://github.com/aadityajain1)    
> [Anirudh Bhaskar](https://github.com/AnirudhBhaskar21)    
> [Srikanth]( https://github.com/Srikanth-AIE)    
> [Rohith Ramakrishnan](https://github.com/Rohith-2)
<hr style=\"border:0.5px solid gray\"> </hr>

## Set-Up:
__Pre-requisites :__ [conda](https://repo.anaconda.com/) and [git](https://git-scm.com/)     
*Please Note : All System Paths in the scripts, are coded in UNIX OS format, please convert '/' to "\\\ " for Windows OS.*
```
git clone https://github.com/Rohith-2/url_classification_dl.git
cd url_classification_dl
conda create -n pyenv python=3.8.5
conda activate pyenv
pip install -r requirements.txt
```
Feature Extraction :    
```
cd scripts/
python extract_Features.py
```
The features extracted are explained and visualised in this [Notebook](https://github.com/Rohith-2/url_classification_dl/blob/main/Notebook/DataProcessing.ipynb). The output training data after feature extraction is labbeled as [features.csv](https://github.com/Rohith-2/url_classification_dl/blob/main/FinalDataset/feature.csv) under FinalDataset. Feature extraction for each category of URLs took on an average 18-26 hours, which extends the total of 95 hours on an average.  
  
Training:
```
cd scripts/
python nn_Training.py
```
The output of the trained model is exported to the [models](https://github.com/Rohith-2/url_classification_dl/blob/main/models).  
  
Testing:
```
cd scripts/
python predict.py
``` 
If you only wish to use the pre-trained model, please check [releases](https://github.com/Rohith-2/url_classification_dl/releases)  
<hr style=\"border:0.5px solid gray\"> </hr>    

Running the GUI locally:
```
cd GUI/
streamlit run predict.py
```
*All the above commands are from the home(url_classification_dl) folder*  
  
## GUI:  
https://share.streamlit.io/rohith-2/url_classification_dl/main/GUI/predict.py  

![Screenshot 2021-05-21 at 12 18 06 PM](https://user-images.githubusercontent.com/55501708/119094445-a8e87280-ba2e-11eb-8241-56c580f073cb.png)  

## Data Description via Extracted Features:
  
![1_YW3D20o-cXrd-WzdYutUNg](https://user-images.githubusercontent.com/55501708/118959890-5b153100-b980-11eb-8c86-71e42c63329b.png)  

  
Plot depecting numerous features normalised(ranging from 0 to 1) and the mean of all the classes. 
![Feature_Plot](https://user-images.githubusercontent.com/55501708/118984429-1f3b9500-b99b-11eb-8ec3-46e264cb95a4.png)

## Performance metric:  
![Screenshot 2021-05-20 at 6 32 01 PM](https://user-images.githubusercontent.com/55501708/118983160-c1f31400-b999-11eb-8fd9-dd54a204f6d0.png)  

<hr style=\"border:0.5px solid gray\"> </hr>   

## Acknowledgment:  
__We would like to thank our professor [Premjith B](https://github.com/premjithb) for the assistance and guidance.__


