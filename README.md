# Multiclass SSL Intrusion Detection for Automotive CAN 

Master's thesis code for injection attacks on automotive CAN traffic
using self supervised pretraining (masked reconstruction) with a downstream 
classification task using XGBoost classifier.  

The encoder is pretrained **only on benign windows**, attack windows are used 
later for supervised evaluation (DoS, Spoofing, Fuzzing, Replay)


```bash
conda create -n ssl-can python=3.13.9 -y
conda activate ssl-can
pip install -r requirements.txt
python -m ipykernel install --user --name ssl-can --display-name "ssl-can"
```

### Dataset
This work uses **CAN-MIRGU** (Rajapaksha et al., 2024).
- Google Drive: https://drive.google.com/drive/folders/1uUKLEu_tFVMy9WkDnf1rqqPwuQLQFwBL?usp=sharing
- GitHub: https://github.com/sampathrajapaksha/CAN-MIRGU

Please cite the dataset as:
```bibtex
@inproceedings{rajapaksha2024can,
  title={CAN-MIRGU: A Comprehensive CAN Bus Attack Dataset from Moving Vehicles for Intrusion Detection System Evaluation},
  author={Rajapaksha, Sampath and Madzudzo, Garikayi and Kalutarage, Harsha and Petrovski, Andrei and Al-Kadri, M Omar},
  booktitle={Symposium on Vehicles Security and Privacy (VehicleSec)},
  year={2024}
}
```

Main log Attacks come from the drive dataset / Attack / Real_attacks + Attacks_metadata.json 
Main log Benign come from the drive dataset / Benign / All folders 

CAN-MIRGU benign logs on Google Drive are split into Benign/, Benign 2/
and Benign 3/ because of file size. That is the same 6 day collection
described in the dataset README as Benign/Day_1 – Day_6.

**SSL pretraining uses three files only**:
- Benign/Day_3/Benign_day3_file1.log
- Benign 2/Day_5/Benign_day5_file1.log
- Benign 2/Day_6/Benign_day6_file1.log

**The 12 .log files are used in 02_File_CrossValidation.ipynb.**

### Environment 
Results in the notebooks were obtained with: 
- **Python 3.13.9**
- **macOS / Apple Silicon**, PyTorch **MPS**
- Packages versions in `requirements.txt`

### Repository Layout 

CNN_Flag/ Encoder: 2 conv layers, no dilation (abliation used in the limitations)

**main_notebooks/**   Main pipeline (EDA, Data Prep, SSL, XGboost)

* embeddings .npy files 
* models .pth files 
* SSL-CNN-30epoch file extended training for model comparison     

Data/ CAN-MIRGU logs, metadata, precomputed windows 

src/  Additional functions needed for the analysis in EDAs 

requirements.txt 

**CNN_Flag/ Is not the final model.** It is the first encoder which was trained (two Conv1d layers no dilation). 
The final encoder is **main_notebooks/04_SSL_Model.ipynb**

To reproduce the abliation metrics, do not retrain. 
Run main_notebooks/05_XGBoost_Evaluation.ipynb which loads the saved embeddings. 

### Weights and .NPY files that exceed > 100MB Download through Google Drive 
https://drive.google.com/drive/folders/1XufzHBmagNbyTTXjKebQ90nN2zbgVsLe?usp=sharing

* Pretrained weights (.pth) 
* XGBoost embeddings (.npy) 
* CNN_Flag: embeddings + model

[Only needed to retrian the SSL or rerun 03_Data_Preparation.ipynb] 

Window Tensors / BenignWindows / AttackWindows

[Day1File2 for Benign EDA (regenerate by 02_Benign_EDA.ipynb if missing)]

Bening_parquet

### IMPORTANT!
In order to reproduce the exact same results it is important to run the notebooks only with the .npy embeddings. 
Not run the main SSL training since Windows (CPU/CUDA) could change the values compared to MPS. 

### How to run 
Follow the order of the numbers set on the files 
01. Attack EDA -> Files: attack .log + metadata
02. Benign EDA -> Files: one benign .log or the parquet
02. File Benign Cross Validation -> Files: all 12 benign .log
03. Data Preparation -> Files: logs → .pt windows
04. SSL Model -> Files: windows or skip and load .pth
05. XGBoost Evaluation -> Files: .npy embeddings

