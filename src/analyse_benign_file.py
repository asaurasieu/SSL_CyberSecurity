from collections import Counter
from file_parser import parse_message

def analyse_benign_file(log_file):
    unique_can_ids = set()
    id_counts = Counter()
    message_count = 0
    first_timestamp = None
    last_timestamp = None

    with open(log_file, "r", errors="ignore") as file:
        for line in file:
            parsed = parse_message(line)
            
            if parsed is None:
                continue
            
            timestamp = parsed["timestamp"]    
            can_id = parsed["can_id"]    

            unique_can_ids.add(can_id)
            id_counts[can_id] += 1
            message_count += 1
            
            if first_timestamp is None:
                first_timestamp = timestamp
            last_timestamp = timestamp

    duration = last_timestamp - first_timestamp
    
    return {
        "file": log_file.name,
        "can_ids": unique_can_ids,
        "id_counts": id_counts,
        "message_count": message_count,
        "duration": duration,
        "message_rate": message_count / duration,
    }
