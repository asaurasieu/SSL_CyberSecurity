import re 

MESSAGE_PATTERN = re.compile(
    r"\((.*?)\)\s+(\S+)\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*(\d*)"
)

def parse_message(message):
    match = MESSAGE_PATTERN.match(message)
    if match is None:
        return None
    
    timestamp = float(match.group(1))
    interface = match.group(2)
    can_id = match.group(3)
    payload = match.group(4)
    flag = match.group(5)
    
    return {
        "timestamp": timestamp,
        "interface": interface,
        "can_id": can_id,
        "payload": payload,
        "flag": flag,
    }