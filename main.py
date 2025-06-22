import csv
import random
from datetime import date

CSV_FILE = 'uids.csv'
HOUSE_PREFIXES = ['PR', 'EK', 'SH', 'SK']
TICKETS_PER_HOUSE = 320

def generate_unique_uid(prefix, existing_uids):
    while True:
        suffix = random.randint(10000, 99999)
        uid = f"{prefix}-{suffix}"
        if uid not in existing_uids:
            return uid

def main():
    existing_uids = set()
    new_entries = []

    for prefix in HOUSE_PREFIXES:
        for _ in range(TICKETS_PER_HOUSE):
            uid = generate_unique_uid(prefix, existing_uids)
            existing_uids.add(uid)
            new_entries.append({
                'uid': uid,
                'updated_at': date.today().isoformat(),
                'used': 'false',
                'house': 'unknown'
            })

    # Overwrite the CSV file
    with open(CSV_FILE, mode='w', newline='') as file:
        fieldnames = ['uid', 'updated_at', 'used', 'house']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for entry in new_entries:
            writer.writerow(entry)

    print(f"✅ Overwrote {CSV_FILE} with {len(new_entries)} fresh UIDs.")

if __name__ == "__main__":
    main()

