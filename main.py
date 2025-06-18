import csv
import os
import random
from datetime import date

CSV_FILE = 'list.csv'

def load_existing_uids():
    existing_uids = set()
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='r', newline='') as file:
            # Peek at the first line to see if it's the header
            first_line = file.readline().strip()
            if 'uid' not in first_line:
                print("⚠️ CSV file doesn't have a valid header. Rewriting with correct headers.")
                # Rewrite the file with header and return empty set
                rows = file.readlines()
                with open(CSV_FILE, mode='w', newline='') as new_file:
                    writer = csv.writer(new_file)
                    writer.writerow(['uid', 'updated_at', 'used'])
                    for row in rows:
                        writer.writerow(row.strip().split(','))
                return existing_uids
            # Rewind to start of file
            file.seek(0)
            reader = csv.DictReader(file)
            for row in reader:
                existing_uids.add(row['uid'])
    return existing_uids


def generate_unique_uid(existing_uids):
    while True:
        uid = str(random.randint(100000, 999999))
        if uid not in existing_uids:
            return uid

def append_uids_to_csv(new_uids):
    file_exists = os.path.exists(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='') as file:
        fieldnames = ['uid', 'updated_at', 'used']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for uid in new_uids:
            writer.writerow({
                'uid': uid,
                'updated_at': date.today().isoformat(),
                'used': 'false'
            })

def main():
    try:
        count = int(input("How many UIDs would you like to generate? "))
    except ValueError:
        print("Please enter a valid number.")
        return

    existing_uids = load_existing_uids()
    new_uids = []

    while len(new_uids) < count:
        uid = generate_unique_uid(existing_uids)
        existing_uids.add(uid)
        new_uids.append(uid)

    append_uids_to_csv(new_uids)
    print(f"{len(new_uids)} UIDs added successfully to {CSV_FILE}.")

if __name__ == "__main__":
    main()
