from file_parser import parse_message

def analyse_attack_file(log_file, attack_start, attack_end):
    complete_file_can_ids = set()
    attack_interval_can_ids = set()

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
            
            complete_file_can_ids.add(can_id)
            if attack_start <= timestamp <= attack_end:
                attack_interval_can_ids.add(can_id)
                
            message_count += 1
            if first_timestamp is None:
                first_timestamp = timestamp
            last_timestamp = timestamp

    return {
        "complete_file_can_ids": complete_file_can_ids,
        "attack_interval_can_ids": attack_interval_can_ids,
        "message_count": message_count,
        "duration": last_timestamp - first_timestamp,
    }
