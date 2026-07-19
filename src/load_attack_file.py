
from pathlib import Path
import json5
import pandas as pd 
import re


BASE = Path("/Users/anita/Documents/TFM/SSL_CyberSecurity")

ATTACK_DIR = BASE / "Attack" / "Real_attacks"
METADATA_PATH = BASE / "Attacks_metadata.json"
DOS_LOG = ATTACK_DIR / "DoS_attack.log"

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



def extract_can_fields(line):
    pattern = r"\((.*?)\)\s+(\S+)\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*(\d*)"
    match = re.match(pattern, line)
    
    if not match: 
        return None 
    
    timestamp, interface, can_id, payload, flag= match.groups()
    
    dlc = len(payload) // 2
    
    payload_bytes = []

    for i in range (0, len(payload), 2): 
        payload_bytes.append(payload[i:i+2])
    
    while len(payload_bytes) < 8: 
        payload_bytes.append("00")
        
    return {
        "timestamp": float(timestamp), 
        "interface": interface, 
        "can_id": can_id, 
        "payload": payload_bytes, 
        "dlc": dlc, 
        "flag": int(flag) if flag else 0, 
    }
    
    
def load_attack_file(name): 
    meta = metadata[name]
    attack_class = ATTACKS[name]
    
    
    path = ATTACK_DIR / f"{name}.log"
    
    rows = []
    with open(path) as f: 
        for line in f: 
            extracted = extract_can_fields(line)
            if extracted is not None: 
                rows.append(extracted)
                
    df = pd.DataFrame(rows)
    
    df["dt"] = df["timestamp"].diff().fillna(0.0)
    
    df["id_int"] = [int(x,16) for x in df["can_id"]]
    
    start, end = meta["injection_interval"]
    
    mask = (
        (df["timestamp"] >= start) & 
        (df["timestamp"] <= end)
    )
    
    df["label"] = "Benign"
    df.loc[mask, "label"] = attack_class
    
    return df 