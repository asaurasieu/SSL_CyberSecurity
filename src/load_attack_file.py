from pathlib import Path
import json5
import pandas as pd
from extract_can_fields import extract_can_fields

BASE = Path(__file__).resolve().parent.parent
ATTACK_DIR = BASE / "Data" / "CAN_MIRGU_Attack_Logs" / "Real_attacks"
METADATA_PATH = BASE / "Data" / "Attacks_metadata.json"

ATTACKS = {
    "Steering_angle_attack": "Spoofing", 
    "Brake_warning_attack": "Spoofing", 
    "Power_steering_attack": "Spoofing", 
    "Min_speedometer_attack_1": "Spoofing", 
    "EMS_replay_attack": "Replay", 
    "Steering_angle_replay": "Replay", 
    "Fuzzing_random_IDs": "Fuzzing", 
    "Fuzzing_valid_IDs": "Fuzzing", 
    "DoS_attack": "DoS",
}

with open(METADATA_PATH) as f:
    metadata = json5.load(f)

def load_attack_file(name):
    path = ATTACK_DIR / f"{name}.log"
    rows = []
    with open(path) as file:
        for line in file:
            row = extract_can_fields(line)
            if row is not None:
                rows.append(row)

    df = pd.DataFrame(rows)
    df["dt"] = df["timestamp"].diff().fillna(0.0)
    df["id_int"] = [int(can_id, 16) for can_id in df["can_id"]]

    df["label"] = "Benign"
    df.loc[df["flag"] == 1, "label"] = ATTACKS[name]

    df = df.drop(columns=["interface"], errors="ignore")
    return df