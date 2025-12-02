import hashlib
import argparse
import os
import glob
import shutil
from datetime import datetime

# --- Hashing Function ---
def get_hash(file_path):
    try:
        with open(file_path, "rb") as f:
            hash_obj = hashlib.sha256()
            while chunk := f.read(8192):
                hash_obj.update(chunk)
            return hash_obj.hexdigest()
    except IOError:
        return None

# --- Process a Single File ---
def process_file(name, active_hashes, log_lines):
    file_hash = get_hash(name)
    if file_hash is None:
        return None

    if name in active_hashes:
        if active_hashes[name] == file_hash:
            return name, file_hash, None
        else:
            log_lines.append(f"[MODIFIED] {datetime.now()}: {name} was modified. Old hash: {active_hashes[name]}, New hash: {file_hash}\n")
            return name, file_hash, 'modified'
    else:
        log_lines.append(f"[CREATED] {datetime.now()}: {name} was created with hash {file_hash}\n")
        return name, file_hash, 'created'

# --- Main FIM Execution ---
def run_fim(requested_file, active_file, temp_file, log_file):
    active_hashes = {}
    log_lines = []

    # Load active file hashes
    if os.path.exists(active_file):
        with open(active_file, 'r') as f:
            for line in f:
                if ' : ' in line:
                    path, hash_val = line.strip().split(' : ', 1)
                    active_hashes[path] = hash_val

    new_active = {}

    # Process requested files
    with open(requested_file, 'r') as req:
        for reqline in req:
            reqline = reqline.strip()
            req_name = os.path.basename(reqline)
            req_dir = os.path.dirname(reqline) + os.sep

            for name in glob.glob(req_dir + req_name):
                result = process_file(name, active_hashes, log_lines)
                if result:
                    fname, fhash, status = result
                    new_active[fname] = fhash

    # Write temporary active file
    with open(temp_file, 'w') as tmp:
        for path, hash_val in new_active.items():
            tmp.write(f"{path} : {hash_val}\n")

    # Write log entries
    if log_lines:
        with open(log_file, 'a') as log:
            for entry in log_lines:
                log.write(entry)

    # Replace old active file
    shutil.copyfile(temp_file, active_file)
    print("[+] File integrity check complete.")

# --- CLI Setup ---
def main():
    parser = argparse.ArgumentParser(description="Simple File Integrity Monitor")
    parser.add_argument('--requested', default='requested.txt', help='File containing list of files to monitor')
    parser.add_argument('--active', default='activefile.txt', help='File to store active known hashes')
    parser.add_argument('--temp', default='activetemp.txt', help='Temporary file for updates')
    parser.add_argument('--log', default='fimlog.txt', help='File to store FIM logs')
    parser.add_argument('--cli', action='store_true', help='Run in CLI mode')
    args = parser.parse_args()

    if args.cli:
        run_fim(args.requested, args.active, args.temp, args.log)
    else:
        print("[-] CLI mode not enabled. Use --cli to run the monitor.")

if __name__ == "__main__":
    main()
