import re

MESSAGE_PATTERN = re.compile(
    r"\((.*?)\)\s+(\S+)\s+([0-9A-Fa-f]+)#([0-9A-Fa-f]*)\s*(\d*)"
)


def analyse_attack_file(log_file, attack_start, attack_end):
    complete_file_can_ids = set()
    attack_interval_can_ids = set()

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
