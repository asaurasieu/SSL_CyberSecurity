from file_parser import parse_message

def extract_can_fields(line):
    parsed = parse_message(line)
    if parsed is None:
        return None

    payload = parsed["payload"]
    payload_bytes = [payload[i:i+2] for i in range(0, len(payload), 2)]
    while len(payload_bytes) < 8:
        payload_bytes.append("00")

    return {
        "timestamp": parsed["timestamp"],
        "interface": parsed["interface"],
        "can_id": parsed["can_id"],
        "payload": payload_bytes,
        "dlc": len(payload) // 2,
        "flag": int(parsed["flag"]) if parsed["flag"] else 0,
    }