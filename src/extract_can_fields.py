import re
from pathlib import Path

BASE = Path("/Users/anita/Documents/TFM/SSL_CyberSecurity")
ATTACK_DIR = BASE / "Attack" / "Real_attacks"
METADATA_PATH = BASE / "Attacks_metadata.json"
DOS_LOG = ATTACK_DIR / "DoS_attack.log"


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