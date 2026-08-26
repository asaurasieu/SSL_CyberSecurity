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
pip install -r requirements.txt
python -m ipykernel install --user --name ssl-can --display-name "ssl-can"
```
---

## Main Structure 
This project uses files from **two different Google Drives**.

| What you need | Source | Link |
|---|---|---|
| **Raw `.log` files** (attack + benign) and `Attacks_metadata.json` | Original **CAN-MIRGU** dataset | https://drive.google.com/drive/folders/1uUKLEu_tFVMy9WkDnf1rqqPwuQLQFwBL | 
| **Precomputed windows** (`BenignWindows`, `AttackWindows`, `.pt` tensors) | **My Drive** | https://drive.google.com/drive/folders/1XufzHBmagNbyTTXjKebQ90nN2zbgVsLe |
| **SSL encoder weights** (`.pth`) and **XGBoost embeddings** (`.npy`) | **My Drive** | same link as above |
| **CNN_Flag** ablation (its embeddings + its model) | **My Drive** | same link as above |


**original logs → dataset Drive. Everything I generated (windows,
weights, embeddings) → my Drive.**

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
  ├─ embeddings/                  SSL embeddings (.npy)      — from my Drive
  └─ cross_file_embeddings/       Cross-file embeddings      — from my Drive

Data/                            Only Attacks_metadata.json on GitHub (rest from Drive)
CNN_Flag/                        Comparison encoder (2 Conv1d, no dilation, 15 epochs)
src/                             Helper functions used by the EDA notebooks
requirements.txt
README.md
.gitignore
```

> On **GitHub**, `main_notebooks/` only the notebooks and `models/`
> (weights). The `embeddings/` and `cross_file_embeddings/` folders are too large
> for GitHub — download them from my Drive (see "Large files" below).

### The Data/ folder

The `Data/` folder **is** on GitHub, but only `Attacks_metadata.json` is committed
there. Everything else inside `Data/` is too large for GitHub and must be
**downloaded from my Drive** and placed into the same folder. The full local
layout is:

```
Data/
  ├─ Attacks_metadata.json       ← committed to GitHub
  ├─ CAN_MIRGU_Attack_Logs/      ← download from the CAN-MIRGU dataset Drive
  │   ├─ Masquerade_attacks/
  │   ├─ Real_attacks/
  │   └─ Suspension_attacks/
  ├─ CAN_MIRGU_Benign_Logs/      ← download from the CAN-MIRGU dataset Drive
  │                                (the 6-day collection, Day_1 … Day_6; the exact
  │                                 subfolder layout depends on how you download)
  ├─ Attack_Windows/             ← download from my Drive  (precomputed .pt)
  └─ Benign_Windows/             ← download from my Drive  (precomputed .pt)
```


> **The original logs are NOT in my Drive.** The `CAN_MIRGU_*_Logs` folders come
> from the original CAN-MIRGU dataset Drive — I just downloaded them into these
> local subfolders. Only the windows I generated (`Attack_Windows`,
> `Benign_Windows`) live in my Drive.


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

### Large files (> 100 MB) — download from my Drive

https://drive.google.com/drive/folders/1XufzHBmagNbyTTXjKebQ90nN2zbgVsLe

- Pretrained SSL weights (`.pth`)
- XGBoost embeddings (`.npy`)
- `CNN_Flag` embeddings + model

Needed only if you want to **retrain the SSL encoder** or **rerun
`03_Data_Preparation.ipynb`**:

- Window tensors (`BenignWindows`, `AttackWindows`)