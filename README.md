# Multiclass SSL Intrusion Detection for Automotive CAN 

Master's thesis code for detecting injection attacks on automotive CAN bus traffic. The approach has two stages:

1. **Self-supervised pretraining** — a CNN encoder is trained with masked
   reconstruction **only on benign windows**, so it learns what normal CAN
   traffic looks like without ever seeing an attack.
2. **Supervised evaluation** — the frozen encoder produces embeddings, and an
   **XGBoost** classifier is trained on top of them to separate benign traffic
   from four attack types: **DoS, Spoofing, Fuzzing, and Replay**.



## Installation

```bash
conda create -n ssl-can python=3.13.9 -y
conda activate ssl-can
python -m pip install -r requirements.txt
python -m ipykernel install --user --name ssl-can --display-name "ssl-can"
```
---

## Main Structure 
This project uses files from Original authors Drive and Dropbox.

| What you need | Source | Link |
|---|---|---|
| **Raw `.log` files** (attack + benign) and `Attacks_metadata.json` | Original **CAN-MIRGU** dataset | https://drive.google.com/drive/folders/1uUKLEu_tFVMy9WkDnf1rqqPwuQLQFwBL | 
| **Precomputed windows** (`BenignWindows`, `AttackWindows`, `.pt` tensors) | **Dropbox** | https://www.dropbox.com/scl/fo/dkud5m4i4ndwm2q4w8tzs/AGLjv3iSLA90cKHipy4g3IQ?rlkey=yb9uhpyyhs03lsinj4dcr7g27&st=10cx5eq7&dl=0 |
| **SSL encoder weights** (`.pth`) and **XGBoost embeddings** (`.npy`) | **Dropbox** | same link as above |
| **CNN_Flag** ablation (its embeddings + its model) | **Dropbox** | same link as above |


**original logs → dataset CAN MIRGU Google Drive. Everything I generated (windows,
weights, embeddings) → Dropbox.**

## Dataset

This work uses **CAN-MIRGU** (Rajapaksha et al., 2024).

- Google Drive: https://drive.google.com/drive/folders/1uUKLEu_tFVMy9WkDnf1rqqPwuQLQFwBL
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

### How the CAN-MIRGU logs are organised

- **Attack logs:** `Attack/Real_attacks/` plus `Attacks_metadata.json`.
- **Benign logs:** in the original CAN-MIRGU Drive they appear as
  `Benign/Day_1 … Day_6`, one folder per day of the 6-day collection.

**SSL pretraining uses three benign files only:**

- `Benign/Day_3/Benign_day3_file1.log`
- `Benign/Day_5/Benign_day5_file1.log`
- `Benign/Day_6/Benign_day6_file1.log`

The **full set of 12 benign `.log` files** is used only in
`File_CrossValidation.ipynb`.

## Repository layout

```
main_notebooks/                  Main pipeline (run in numeric order)
  ├─ 01_Attack_EDA.ipynb
  ├─ 02_Benign_EDA.ipynb
  ├─ 02_File_CrossValidation.ipynb
  ├─ 03_Data_Preparation.ipynb
  ├─ 04_SSL_Model.ipynb           Final SSL encoder
  ├─ 05_XGBoost_Evaluation.ipynb
  ├─ SSL-CNN_30epochs.ipynb       Extended training (30 epochs), comparison
  ├─ models/                      Pretrained weights (.pth)  — on GitHub
  ├─ embeddings/                  SSL embeddings (.npy)      — from Dropbox
  └─ cross_file_embeddings/       Cross-file embeddings      — from Dropbox

Data/                            Attacks_metadata.json on GitHub; logs from CAN-MIRGU Drive; windows from Dropbox
CNN_Flag/                        Comparison encoder (2 Conv1d, no dilation, 15 epochs)
src/                             Helper functions used by the EDA notebooks
requirements.txt
README.md
.gitignore
```

> Each data folder in this repo contains a `dummy.txt`. That file is only there
> so Git keeps the original directory tree. **Jupyter Notebooks (including on
> Windows) does not let the Upload button add a whole folder** — you must open
> an existing folder and upload **files** into it. After cloning, the original
> folders are already there; unzip your downloads and put the files inside those
> folders, next to `dummy.txt`. Do not rename the files and do not delete
> `dummy.txt`.

### Unzip and place the files

Clone first, then unzip. Open the matching folder that already exists and upload
or copy **the files** into it (not the parent ZIP folder).

**CAN-MIRGU logs** (Google Drive, not Dropbox):

1. Unzip the authors' attack download. This pipeline only uses **Real attacks**,
   and only these **9** `.log` files in `Data/CAN_MIRGU_Attack_Logs/Real_attacks/`:
   `Steering_angle_attack.log`, `Brake_warning_attack.log`,
   `Power_steering_attack.log`, `Min_speedometer_attack_1.log`,
   `EMS_replay_attack.log`, `Steering_angle_replay.log`,
   `Fuzzing_random_IDs.log`, `Fuzzing_valid_IDs.log`, `DoS_attack.log`.
   You do **not** need the rest of the Real_attacks logs.
   `Masquerade_attacks/` and `Suspension_attacks/` are in the clone (with
   `dummy.txt`) so the original CAN-MIRGU layout is there if you want those
   logs; they are **not required** to run the notebooks.
2. Unzip all benign ZIP parts (Drive may split them). Open
   `Data/CAN_MIRGU_Benign_Logs/Benign/Day_1` … `Day_6` and put each `.log` into
   the matching day folder.

**Dropbox** (windows, embeddings):

| After unzipping, put these files | Into this existing folder |
|---|---|
| Attack `.pt` windows | `Data/Attack_Windows/` |
| `Benign_day3_file1_*.pt` | `Data/Benign_Windows/BenignDay3/` |
| `Benign_day5_file1_*.pt` | `Data/Benign_Windows/BenignDay5/` |
| `Benign_day6_file1_*.pt` | `Data/Benign_Windows/BenignDay6/` |
| `X_*.npy` / `y_*.npy` (cnn_15 and cnn_30) | `main_notebooks/embeddings/` |
| `*_cross_embedding.npy` | `main_notebooks/cross_file_embeddings/` |
| `X_*_15.npy` / `y_*_15.npy` | `CNN_Flag/embeddings/` |

```
Data/
  ├─ Attacks_metadata.json       ← already on GitHub
  ├─ CAN_MIRGU_Attack_Logs/
  │   ├─ Masquerade_attacks/      ← optional (not used by the notebooks)
  │   ├─ Real_attacks/            ← only the 9 .log files listed above
  │   └─ Suspension_attacks/      ← optional (not used by the notebooks)
  ├─ CAN_MIRGU_Benign_Logs/      ← unzip benign .log files here
  │   └─ Benign/Day_1 … Day_6/
  ├─ Attack_Windows/             ← unzip attack .pt files here
  └─ Benign_Windows/
      ├─ BenignDay3/             ← unzip day-3 .pt files here
      ├─ BenignDay5/
      └─ BenignDay6/
```

> **The original logs are NOT in Dropbox.** They come from the CAN-MIRGU
> Google Drive. Only the windows and embeddings I generated are in Dropbox.


### The final model vs. the comparison encoders

- **Final encoder:** `main_notebooks/04_SSL_Model.ipynb`. This is the model
  reported in the thesis.
- **`SSL-CNN_30epochs.ipynb`:** the same SSL-CNN trained for longer (30 epochs),
  kept only for model comparison.
- **`CNN_Flag/`:** an earlier encoder — two `Conv1d` layers with **no dilation**,
  trained for **15 epochs**. Used **only as a comparison inside
  `05_XGBoost_Evaluation.ipynb`**, and **not reported in the paper/thesis**.

To reproduce the comparison metrics, **do not retrain**. Run
`05_XGBoost_Evaluation.ipynb`, which loads the saved embeddings.

---

## How to run

Run the notebooks in the order of their number prefix.

| Notebook | Input it needs |
|---|---|
| `01_Attack_EDA.ipynb` | Attack `.log` files + `Attacks_metadata.json` |
| `02_Benign_EDA.ipynb` | One benign `.log` |
| `02_File_CrossValidation.ipynb` | All 12 benign `.log` files |
| `03_Data_Preparation.ipynb` | Logs → produces `.pt` windows |
| `04_SSL_Model.ipynb` | Benign windows, or skip and load the `.pth` |
| `05_XGBoost_Evaluation.ipynb` | `.npy` embeddings |

`SSL-CNN_30epochs.ipynb` is not part of the main sequence — run it only if you
want the extended-training model used for comparison.

---

## Reproducibility

Results in the notebooks were obtained with:

- **Python 3.13.9**
- **macOS / Apple Silicon**, PyTorch **MPS** backend
- Package versions pinned in `requirements.txt`

> **Important:** to reproduce the exact numbers, run the pipeline from the saved
> `.npy` embeddings and do **not** retrain the SSL encoder. Retraining on a
> different backend (CPU or CUDA) can produce slightly different values than the
> MPS run.

### Large files (> 100 MB) — download from the Dropbox link

https://www.dropbox.com/scl/fo/dkud5m4i4ndwm2q4w8tzs/AGLjv3iSLA90cKHipy4g3IQ?rlkey=yb9uhpyyhs03lsinj4dcr7g27&st=10cx5eq7&dl=0

Unzip the archive, then in Jupyter open the existing folder and use **Upload**
for the files (not the folder). The `dummy.txt` in each directory is what makes
that folder appear after a clone.

- XGBoost embeddings (`.npy`) → `main_notebooks/embeddings/` and `cross_file_embeddings/`
- `CNN_Flag` embeddings (`.npy`) → `CNN_Flag/embeddings/`

Needed only to **retrain** the SSL encoder or **rerun** `03_Data_Preparation.ipynb`:

- Window tensors (`.pt`) → `Data/Attack_Windows/` and `Data/Benign_Windows/BenignDay3` … `BenignDay6`