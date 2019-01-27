#!/usr/bin/env python3

import csv
import os

num_users = 15
num_conditions = 3
num_tasks = 6

"""
    For the given path, get the List of all files in the directory tree.
    (Source): https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
"""
def create_file_list(directory):
    # Create list of file and sub directories.
    file_list = os.listdir(directory)
    all_files = list()

    for entry in file_list:
        # Create full path for entry.
        fullpath = os.path.join(directory, entry)

        # If entry is a directory, get list of files in it.
        if (os.path.isdir(fullpath)):
            all_files = all_files + create_file_list(fullpath)
        else:
            all_files.append(fullpath)
    
    return all_files

def filter_user_data(file_paths):
    user_paths = list(filter(lambda s: s.split('/')[1].startswith("user"), file_paths))
    data_paths = list(filter(lambda s: s.split('/')[2].startswith("data"), user_paths))
    return data_paths

def get_user_id(path):
    user_string = list(filter(lambda s: s.startswith("user"), path.split('/')))[0]
    return int(user_string.split('_')[1])

def get_condition_id(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return int(filename.split('_')[2])

def get_task_id(path):
    filename = os.path.splitext(os.path.basename(path))[0]
    return int(filename.split('_')[4])

def record_to_csv(path):
    values = list()

    with open(path, "r") as file:
        data = list(filter(None, (line.rstrip() for line in file)))
        for entry in data:
            values.append(entry.split(": ")[1])

    return values

def record_csv_header(path):
    keys = list()

    with open(path, "r") as file:
        data = list(filter(None, (line.rstrip() for line in file)))
        for entry in data:
            keys.append(entry.split(": ")[0])

    return keys


def main():
    paths = filter_user_data(create_file_list("."))

    with open("results.csv", "w", newline="") as csvfile:
        resultwriter = csv.writer(csvfile)

        # Write header to csv file (just pick any record for that).
        resultwriter.writerow(["User ID"] + record_csv_header(paths[0]))

        for user in range(0, num_users):
            for condition in range(0, num_conditions):
                for task in range(0, num_tasks):
                    record_path = next(x for x in paths if (get_user_id(x) == user and get_condition_id(x) == condition and get_task_id(x) == task))

                    resultwriter.writerow([user] + record_to_csv(record_path))

if __name__ == "__main__":
    main()
