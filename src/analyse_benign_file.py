import re
from collections import Counter

MESSAGE_PATTERN = re.compile(
    r"\((.*?)\)\s+(\S+)\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*(\d*)"
)


def analyse_benign_file(log_file):
    unique_can_ids = set()
    id_counts = Counter()

    message_count = 0
    first_timestamp = None
    last_timestamp = None

    with open(log_file, "r", errors="ignore") as file:
        for line in file:
            match = MESSAGE_PATTERN.match(line)
            if match is None:
                continue

            timestamp = float(match.group(1))
            can_id = match.group(3).upper()

            unique_can_ids.add(can_id)
            id_counts[can_id] += 1
            message_count += 1

            if first_timestamp is None:
                first_timestamp = timestamp

            last_timestamp = timestamp

    duration = last_timestamp - first_timestamp
    message_rate = message_count / duration
    mean_dt = duration / (message_count - 1)

    return {
        "file": log_file.name,
        "can_ids": unique_can_ids,
        "id_counts": id_counts,
        "message_count": message_count,
        "duration": duration,
        "message_rate": message_rate,
        "mean_dt": mean_dt,
    }
